import os
from flask import Flask, render_template, url_for, session, request, json, redirect,flash

app = Flask(__name__)
app.secret_key = os.getenv("SECRET", "not a secret")

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
    
@app.route('/game', methods = ['GET','POST'])
def game():
    '''
    User must have inserted the username in order to play
    '''
    if 'username' not in session:
        return redirect ('/')
    '''
    check if the previously asked question was the last and if the given answer was correct
    '''
    if request.method == "POST" and session['question_number'] < len(questions):
        prev_qa_tuple = questions[session['question_number']]
        if request.form['answer'] == prev_qa_tuple['answer']:
            flash('CORRECT')
            session['question_number'] +=1
            session['score'] +=1
            '''
            check if there are more questions to ask and show the next question
            '''
            if session['question_number'] < len(questions):
                current_qa_tuple = questions[session['question_number']]
                return render_template('game.html', username = session['username'], 
                                        score = session['score'], current_question = current_qa_tuple["question"], 
                                        question_number = session ['question_number'] + 1, attempts = session['attempts_left'])
        elif session['attempts_left'] > 1 :
            session['attempts_left']-= 1
            flash('WRONG')
            return render_template('game.html', username = session['username'], 
                                        score = session['score'], current_question = prev_qa_tuple["question"], 
                                        question_number = session ['question_number'] + 1, attempts = session['attempts_left'])
        elif session['attempts_left'] <= 1:
            session['attempts_left'] = max_attempts
            session['question_number'] +=1
            next_qa_tuple = questions[session['question_number']]
            flash('Try a different question')
            return render_template('game.html', username = session['username'], 
                                        score = session['score'], current_question = next_qa_tuple["question"], 
                                        question_number = session ['question_number'] + 1, attempts = session['attempts_left'])
        
        
    if session['question_number'] >= len(questions):
        return redirect ('/')
        
    
    '''
    New Game 
    '''
    first_qa_tuple = questions[session['question_number']]
    return render_template('game.html', username = session['username'], 
                            score = session['score'], current_question = first_qa_tuple["question"], 
                            question_number = session ['question_number'] + 1, attempts = session['attempts_left'])


    
@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

if __name__ == '__main__':
    app.run(host = os.getenv('IP'), 
            port = int(os.getenv('PORT')),
            debug = True)  