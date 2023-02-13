from flask import Flask, request, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tastycakes'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def home_survey():
    return render_template('home.html', survey=survey)

@app.route('/begin', methods=['POST'])
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')


@app.route('/answer', methods=["POST"])
def handle_question():
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses
    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/questions/<int:qid>')
def show_question(qid):
    responses = session.get(RESPONSES_KEY)
    if (responses is None):
        return redirect('/')
    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    if (len(responses) != qid):
        flash(f"Invalid Question ID: {qid}")
        return redirect(f"/questions/{len(responses)}")
    question = survey.questions[qid]
    return render_template('question.html', question_num=qid, question=question)


@app.route('/complete')
def completed_form():
    return render_template('complete.html')
