import re

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, abort, app
from config import Config
from models import db, User, Message, ReceivedMessage
from flask_login import LoginManager, current_user, login_required
from auth import bp as auth_bp
import os


login_manager = LoginManager()
login_manager.login_view = None
login_manager.login_message = None

@login_manager.unauthorized_handler
def unauthorized():
    return abort(403)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403


    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('405.html'), 405


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    @app.route('/admin')
    @login_required
    def admin():
        if not current_user.is_authenticated or not current_user.is_admin:
            return render_template('base.html', message='Accès refusé: permissions insufisantes'), 403
        return render_template('admin.html', flag=Config.FLAG)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        if request.method == 'POST':
            content = request.form.get('content', '').strip()

            if content:
                msg = Message(user_id=current_user.id, content=content)
                db.session.add(msg)
                db.session.commit()
        messages = Message.query.order_by(Message.timestamp.asc()).all()
        return render_template('chat.html', messages=messages)

    @app.route('/api/messages')
    @login_required
    def get_messages():
        messages = Message.query.order_by(Message.timestamp.asc()).all()
        result = []
        for msg in messages:
            result.append({
                "id": msg.id,
                "content": msg.content,
                "timestamp": msg.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
                "user": {
                    "name": msg.user.name,
                    "email": msg.user.email,
                    "profile_picture_url": msg.user.profile_picture_url
                }
            })
        return jsonify(result)

    @app.route('/api/messages', methods=['POST'])
    @login_required
    def post_message():
        data = request.get_json()
        content = data.get('content')

        msg = Message(content=content, user_id=current_user.id)
        db.session.add(msg)
        db.session.commit()
        return jsonify({"success": True})

    def is_valid_image_url(url):
        pattern = re.compile(r'^https?://.*\.(png|jpg|jpeg|gif)$', re.IGNORECASE)
        return pattern.match(url)

    @app.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html')

    @app.route('/profile/upload', methods=['POST'])
    @login_required
    def update_profile_picture():
        image_url = request.form.get('profile_picture_url', '').strip()

        if not image_url:
            flash("Veuillez saisir une URL.", "error")
            return redirect(url_for('profile'))

        if not is_valid_image_url(image_url):
            flash("L'URL doit être une image valide (png, jpg, jpeg, gif).", "error")
            return redirect(url_for('profile'))

        # Met à jour l'URL de la photo dans la base
        current_user.profile_picture_url = image_url
        db.session.commit()

        flash("Photo de profil mise à jour avec succès !", "success")
        return redirect(url_for('profile'))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/api/received_messages')
    @login_required
    def get_received_messages():
        messages = ReceivedMessage.query.filter_by(recipient_id=current_user.id).order_by(
            ReceivedMessage.timestamp.desc()).all()
        data = [
            {
                "id": m.id,
                "content": m.content,
                "sender_name": m.sender,
                "read": m.read,
                "timestamp": m.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
            }
            for m in messages
        ]
        return jsonify(data)

    @app.route('/api/received_messages/mark_read', methods=['POST'])
    @login_required
    def mark_messages_read():
        messages = ReceivedMessage.query.filter_by(recipient_id=current_user.id, read=False).all()
        for m in messages:
            m.read = True
        db.session.commit()
        return jsonify({"status": "ok"})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)