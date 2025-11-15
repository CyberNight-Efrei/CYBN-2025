from flask import Flask, render_template, redirect, url_for, session
import secrets
import time
import os

app = Flask(__name__)
app.secret_key = 'LeGrosZiziDeNozouille' # Personne viendra chercher de toute façon donc menfou

valid_urls = {}

@app.route('/')
def index():
    session.clear()
    session['user_id'] = secrets.token_urlsafe(16)
    session['score'] = 0
    session['start_time'] = time.time()
    
    first_url = generate_new_url(session['user_id'])
    return render_template('chase.html', next_url=first_url, score=0, elapsed_time=0.0)

def generate_new_url(user_id):
    url_key = secrets.token_urlsafe(16)
    valid_urls[url_key] = {
        'user_id': user_id,
        'created_at': time.time()
    }
    return f'/{url_key}'

@app.route('/<path:url_key>')
def chase_ferret(url_key):
    current_time = time.time()
    if url_key not in valid_urls:
        return redirect(url_for('fail'))
    url_data = valid_urls[url_key]
    if session.get('user_id') != url_data['user_id']:
        session['user_id'] = url_data['user_id']
        session['score'] = 0
    
    if current_time - url_data['created_at'] > 0.7:
        return redirect(url_for('fail'))
    
    del valid_urls[url_key]
    
    session['score'] += 1
    session['current_step'] = session.get('current_step', 1) + 1
    if session['score'] >= 10:
        final_time = current_time - session['start_time']
        return render_template('success.html', score=session['score'], time=round(final_time, 2), flag=os.getenv('FLAG'))
    
    next_url = generate_new_url(session['user_id'])
    
    return render_template('chase.html', next_url=next_url, score=session['score'], elapsed_time=round(current_time - session['start_time'], 2))
    

@app.route('/fail')
def fail():
    return render_template('fail.html', score=session.get('score', 0))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
