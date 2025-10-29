from datetime import datetime, timedelta

from app import create_app
from config import Config
from models import db, User, Message, ReceivedMessage
from random import uniform
import secrets

app = create_app()

MAIL = "sandwicherie.fr"

with app.app_context():
    db.create_all()
    # Admin initial
    admin_email = f'admin@{MAIL.lower()}'
    admin_password = 'admin'
    if not User.query.filter_by(email=admin_email).first():
        admin = User(email=admin_email, name='admin', is_admin=True)
        admin.set_password(Config.ADMIN_PASSWORD)
        db.session.add(admin)
        print(f'Admin created: {admin_email} : {admin_password} ')
    else:
        print('Admin alrerady exists')

    # Nouveaux utilisateurs
    users_info = [
        {'name': 'Pain', 'picture': 'https://www.delifrance.com/media/catalog/product/cache/a9b648c4a69ecedf0b53157585ebface/s/2/s2144_1.jpg'},
        {'name': 'Salade', 'picture': 'https://img.freepik.com/photos-premium/feuilles-fraiches-salade-verte-isolees-fond-blanc-vue-du-haut_253984-7107.jpg'}
    ]
    for user_info in users_info:
        email = f'{user_info['name'].lower()}@{MAIL.lower()}'
        if not User.query.filter_by(email=email).first():
            user = User(email=email, name=user_info['name'], profile_picture_url=user_info['picture'], is_admin=False)
            password = secrets.token_urlsafe(8)
            user.set_password(password)
            db.session.add(user)
            print(f'Utilisateur créé: {email} / {password}')

            db.session.commit()

        else:
            print(f'Utilisateur already exists: {email}')

    # Ajouter des messages initiaux sur le monde du sandwich
    all_users = User.query.all()

    messages = [
        {
            "author": all_users[1].email,
            "content": "Trop bien la sandwicherie ! Enfin un endroit où je me sens à ma place !\n\nY'a qui d'autre ici ?"
        },
        {
            "author": all_users[2].email,
            "content": "Oh salut toi, comme on se retrouve !\n\nAlors il était comment ton dernier SoubWay ? Parce que le mien pas terrible terrible..."
        },
        {
            "author": all_users[1].email,
            "content": "Salut, content de te revoir !\nBah il était vraiment pas ouf... Même complètement dégueu, c'était vraiment HORRIBLE PUTAIN!! Plus jamais je bosse là-bas, le mec en avait déjà pleins les dents... J'te raconte pas..."
        },
        {
            "author": admin_email,
            "content": "Langage."
        },
        {
            "author": all_users[1].email,
            "content": "Ouhla, euh... ok... pardon"
        },
        {
            "author": all_users[2].email,
            "content": "Ouais il est un peu rude... Tu comprends, il vient des meilleurs ouvriers de France... bref tout un délire...\n\nOn peut décaler MP, je pense pas que fromage arrive de sitôt..."
        },
        {
            "author": all_users[1].email,
            "content": "Ca roule."
        },
    ]

    base_time = datetime.now() - timedelta(minutes=10)  # exemple : 10 minutes dans le passé

    for i in range(len(messages)):
        delay = uniform(15, 70)
        timestamp = base_time + timedelta(seconds=delay)
        user = User.query.filter_by(email=messages[i]['author']).first()
        message = Message(user_id=user.id, content=messages[i]['content'], timestamp=timestamp)
        db.session.add(message)
        base_time = timestamp

        db.session.commit()

    print('Messages initiaux ajoutés pour tous les utilisateurs.')

    existing_message = ReceivedMessage.query.filter_by(recipient_id=admin.id).first()

    if not existing_message:
        welcome_message = ReceivedMessage(
            content="La Sandwicherie est prête à être dévorée !",
            recipient_id=admin.id,
            read=True,
            timestamp=datetime.now()
        )
        db.session.add(welcome_message)
        db.session.commit()
        print("Message de bienvenue créé pour l'admin")
    else:
        print("L'admin a déjà reçu un message, aucun nouveau message créé")