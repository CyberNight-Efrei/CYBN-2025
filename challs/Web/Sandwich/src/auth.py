from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user

from config import Config
from models import db, User, PasswordResetToken

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        name = request.form['name'].strip()
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Un compte existe déjà avec cet email.', 'warning')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(name=name).first():
            flash('Un compte existe déjà avec ce nom d\'utilisateur.', 'warning')
            return redirect(url_for('auth.register'))
        user = User(email=email, name=name)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        flash('Compte créé — vous pouvez vous connecter.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name'].strip().lower()
        password = request.form['password']
        user = User.query.filter_by(name=name).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Connecté.', 'success')
            return redirect(url_for('index'))
        flash('Email ou mot de passe incorrect.', 'error')
    return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Déconnecté.', 'info')
    return redirect(url_for('auth.login'))


# Reset password request
@bp.route('/reset-request', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        user = User.query.filter_by(email=email).first()
        if user:
            PasswordResetToken.generate(user, expiration_minutes=Config.DEFAULT_TOKEN_EXPIRATION_MINUTES)
            flash('Si cet email existe, un message de réinitialisation a été envoyé.', 'info')
        else:
            # Ne pas révéler l'existence du compte
            flash('Si cet email existe, un message de réinitialisation a été envoyé.', 'info')
            return redirect(url_for('auth.login'))
    return render_template('reset_request.html')


@bp.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = PasswordResetToken.verify(token)
    if not user:
        flash('Token invalide ou expiré.', 'error')
        return redirect(url_for('auth.reset_request'))
    if request.method == 'POST':
        password = request.form['password']
        user.set_password(password)
        reset_token = PasswordResetToken.query.filter_by(token=token).first()
        if reset_token:
            reset_token.is_used = True
        db.session.commit()
        flash('Mot de passe mis à jour. Vous pouvez vous connecter.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', valid=user is not None)