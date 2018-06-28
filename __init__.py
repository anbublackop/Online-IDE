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

	endpoint_run = "https://api.jdoodle.com/v1/execute"
	clientId = "ac4680b2f667cd4864a60e9d5cd4d18f"
	client_secret_key = "4a941cc902adaca23c1e67330856b697726c68f84c5a88ccd1bf5c4cb7568ea3"

	source = request.form["source"]
	input_received = request.form["input"]

	data = {
    'clientSecret': client_secret_key,
    'clientId': clientId,
    'script': source,
    'stdin': input_received,
    'language': "python3",
    'versionIndex': '2'
	}	

	response = requests.post(endpoint_run, json=data)

	return render_template('main.html', Result = response.text)

if __name__== '__main__':
	app.run(debug = True)