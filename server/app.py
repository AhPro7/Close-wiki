from flask import Flask, render_template, request
from Close import api

app = Flask(__name__)

# set static folder and template folder
app.static_folder = 'static'
app.template_folder = 'templates'


@app.get('/')
def index():
    # render index.html
    return render_template('index.html')


@app.post('/ask')
def ask():
    # gets the input from JSON
    prompt = request.json['prompt']

    # call the api
    answer = api.ask(prompt)

    # return the response
    return {
        'response': answer
    }

