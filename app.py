from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'greentreemonitor1357'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

global survey_complete
survey_complete = False
SURVEY = satisfaction_survey
RESPONSES  = []

@app.after_request
def after_request(response):
    """
    Prevents cached responses from the server
    https://stackoverflow.com/questions/47376744/how-to-prevent-cached-response-flask-server-using-chrome
    """
    response.headers["Cache-Control"] = "public no-cache, no-store, must-revalidate, max-age=0, post-check=0, pre-check=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = 0
    return response

@app.route('/')
def home_page():
    # app.logger.info('RESPONSES length: %s', len(RESPONSES))
    return render_template('home.html', survey=SURVEY)

@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html', survey=SURVEY)

@app.route('/sorry')
def sorry():
    return render_template('sorry.html', survey=SURVEY)

@app.route('/questions/<int:num>', methods=['POST', 'GET'])
def question_page(num):
    questions = SURVEY.questions
    responses_length = len(RESPONSES)
    questions_length = (len(list(SURVEY.questions)))
    global survey_complete
    if(survey_complete):
        return redirect('/thankyou')
    if(request.method == 'POST'):
        if(num == responses_length):
            if(num > questions_length):
                return redirect('/sorry')
            elif(num == questions_length):
                RESPONSES.append(request.form.get('input'))
                RESPONSES.pop(0)
                survey_complete = True
                return redirect('/thankyou')
            else:
                RESPONSES.append(request.form.get('input'))
                return redirect(f'/questions/{num}')
                # return render_template('questions.html', questions=questions, num=num)
        else:
            if(responses_length == questions_length):
                return redirect('/thankyou')
            else:
                return redirect('/sorry')
    else:
        if(responses_length > 0):
            if(num != responses_length-1):
                flash('Page redirected: Attempt to access an invalid question')
            return render_template('questions.html', questions=questions, num=responses_length-1)
        elif(responses_length == questions_length):
            return redirect('/')
        else:
            return redirect('/sorry')

########################################################
########################################################

# COUNT_QUESTIONS = [1,2,3,4]
# RESPONSES_LIST = []
# @app.route('/debug/<int:num>', methods=['POST', 'GET'])
# def debug_route(num):
#     responses_length = len(RESPONSES_LIST)
#     count_length = len(COUNT_QUESTIONS)
#     if(request.method == 'POST'):
#         import pdb;  pdb.set_trace()
#         if(num == responses_length and num < count_length):
#             RESPONSES_LIST.append(COUNT_QUESTIONS[num])
#             return render_template('debug.html', count_questions=COUNT_QUESTIONS, num=responses_length)
#         else:
#             if(responses_length == count_length):
#                 return 'thank you'
#             else:
#                 return 'error'
#     else:
#             import pdb;  pdb.set_trace()
#             if(responses_length == count_length):
#                 return 'thank you'
#             else:
#                 return 'error'