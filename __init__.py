from flask import Flask, render_template
from flask import Flask, redirect, url_for, request, render_template, session, escape, abort, flash, send_from_directory
import sys, requests, json

app = Flask (__name__)

@app.route('/')
def home():
	return render_template ('main.html')

@app.route('/homepage/')
def Homepage():
	return "This is Homepage"

@app.route('/Login/')
def login():
	return render_template('Login.html')

@app.route('/compile_and_run/', methods = ['POST'])
def compile_and_run():

	endpoint_run = "http://api.hackerearth.com/code/run/"
	client_secret_key = "71f2e0924665da501e290e3a2d831581a9f3a451"

	source = request.form['source']

	data = {
    'client_secret': client_secret_key,
    'async': 0,
    'source': source,
    'lang': "PYTHON",
    'time_limit': 5,
    'memory_limit': 262144,
	}

	response = requests.post(endpoint_run, data = data)

	return render_template('main.html', Result = response.text)

if __name__== '__main__':
	app.run(debug = True)