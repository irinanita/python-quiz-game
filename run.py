import os
from flask import Flask, render_template, url_for, session, request, json, redirect,flash

app = Flask(__name__)
app.secret_key = os.getenv("SECRET", "not a secretgit pu")

max_attempts = 3
with open("data/questions.json") as questions_file:
    questions = json.load(questions_file)

high_score = {
    "name": "noname",
    "score": 0
}

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/start_game', methods = ['POST'])
def start_game():
    session['username']= request.form['username']
    session['score'] = 0
    session['question_number']= 0
    session['attempts_left'] = max_attempts
    return redirect ('/game') 

@app.route('/game_over')
def game_over():
    return render_template('game_over.html')
    
@app.route('/game', methods = ['GET','POST'])
def game():
    '''
    User must have inserted a username in order to play
    '''
    if 'username' not in session or session['username'] == "" :
        flash('Please insert a username')
        return redirect ('/')
    '''
    
    check if the previously asked question was the last and if the given answer was correct
    '''
    
    if request.method == "POST" and session['question_number'] < len(questions):
        option_checked =  request.form['option']
        print(option_checked)
        prev_qa_tuple = questions[session['question_number']]
        print(prev_qa_tuple['answer'])
        # if option_checked == prev_qa_tuple['answer']:
        #     session['score'] +=1
        #     session['question_number'] +=1
        #     if session['question_number'] < len(questions):
        #         flash('Correct Answer')
        # else:
        #     flash('Wrong Answer')
        #     session['question_number'] +=1
        
    if session['question_number'] >= len(questions):
        return render_template('game_over.html', username = session['username'], score = session['score'])
        
    '''
    New Game 
    '''
    current_qa_tuple = questions[session['question_number']]
    options = current_qa_tuple['options']
    return render_template('game.html', username = session['username'],
                            questions = questions, options = options,
                            score = session['score'], current_question = current_qa_tuple["question"], 
                            question_number = session ['question_number'] + 1, attempts = session['attempts_left'])

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

if __name__ == '__main__':
    app.run(host = os.getenv('IP'), 
            port = int(os.getenv('PORT')),
            debug = True)  