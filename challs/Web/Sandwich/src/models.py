from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from uuid import uuid1
from config import Config

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    profile_picture_url = db.Column(db.String(), default='https://d2jbk7d41q2u2w.cloudfront.net/uploads/recipe/image/27/medium_thumb_61788c6817cad2fbd241bae09c8880b0-1558497960.jpg')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(128), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False, nullable=False)

    user = db.relationship('User', backref=db.backref('reset_tokens', lazy=True))

    @staticmethod
    def generate(user, expiration_minutes=Config.DEFAULT_TOKEN_EXPIRATION_MINUTES):
        token_str = str(uuid1(clock_seq=0))
        expires = datetime.now() + timedelta(minutes=expiration_minutes)
        token = PasswordResetToken(token=token_str, user_id=user.id, expires_at=expires)
        db.session.add(token)

        reset_link = url_for('auth.reset_password', token=token.token, _external=True)

        message_content = f'Vous avez demandé une réinitialisation de votre mot de passe. Cliquez ici pour réinitialiser votre mot de passe : <a href="{reset_link}">{reset_link}</a>. Ce lien est valide pendant {Config.DEFAULT_TOKEN_EXPIRATION_MINUTES} minutes.'
        received_message = ReceivedMessage(
            content=message_content,
            recipient_id=user.id,
            read=False,
            timestamp=datetime.now()
        )
        db.session.add(received_message)
        db.session.commit()

        return token

    @staticmethod
    def verify(token_str: str):
        token = PasswordResetToken.query.filter_by(token=token_str).first()
        if not token or token.is_used or token.expires_at < datetime.now():
            return None
        return token.user

    def __repr__(self):
        return f'<PasswordResetToken user={self.user_id} expires={self.expires_at}>'

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', backref=db.backref('messages', lazy=True))

    def __repr__(self):
        return f'<Message user={self.user_id} timestamp={self.timestamp}>'

class ReceivedMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    sender = db.Column(db.String(32), default="no-reply@sandwicherie.fr")

    recipient = db.relationship("User", foreign_keys=[recipient_id])