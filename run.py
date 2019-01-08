import os
from flask import Flask, render_template, url_for, session, request

app = Flask(__name__)
app.secret_key = os.getenv("SECRET", "not a secret")

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/game', methods = ['POST'])
def game():
    session['username']= request.form['username']
    return render_template('game.html', username = session['username'])
    
@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

if __name__ == '__main__':
    app.run(host = os.getenv('IP'), 
            port = int(os.getenv('PORT')),
            debug = True)  