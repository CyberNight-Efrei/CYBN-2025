from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('home.html')

# Patch the champ c'est du troll pour ragebait les mecs qui trouveront malin
# d'aller regarder ce qu'il se passe là bas 
# en get on les troll, en patch aussi et en post on fait joujou avec leurs nerfs

@app.route('/patch-the-champ', methods=['POST', 'PATCH', 'GET','DELETE', 'OPTIONS'])
def patch_the_champ():
    if request.method == 'POST':
        flag = None
        html = '<img src="https://http.cat/images/400.jpg" alt="hehe" />'
        return html, 200
    if request.method == 'GET':
        flag = None
        return render_template('troll.html')
    elif request.method == 'PATCH':
        flag = None
        html = '<img src="https://http.cat/images/405.jpg" alt="hehe" />'
        return html, 200
# Pour les html bizarre c'est normal, http.cat bloque les .patch donc je get l'image
# comme ça...

# ----------------- Now the serious shit -----------------------------

@app.route('/delete-the-champ', methods=['DELETE', 'GET', 'OPTIONS', 'MOT_DE_PASSE_ADMIN'])
def delete_the_champ():
    headers_to_return = {
            'Allow': 'DELETE, GET, OPTIONS, MOT_DE_PASSE_ADMIN'
    }
    if request.method == 'DELETE':
        if request.values.get('password') == 'N0zzyLePlusBeau-1234':
            to_return = os.environ.get('FLAG', 'Une erreur est survenue, contactez les admins sur discord.')
        else:
            flag = None
            to_return = ("Je suis presque sûr qu'il faut un mot de password dans le body pour faire un truc pareil...", 401)
        return to_return
    if request.method == 'OPTIONS':
        flag = None
        return(204, headers_to_return)
    if request.method == 'MOT_DE_PASSE_ADMIN':
        flag = None
        return ("mot de passe de l'admin : N0zzyLePlusBeau-1234")
    if request.method == 'GET':
        flag = None
        html = '<img src="https://http.cat/images/400.jpg" alt="hehe" />'
        return html, 400

        
if __name__ == '__main__':
    app.run()
