from flask import Flask, render_template, jsonify	
from flask import Flask, redirect, url_for, request, render_template, session, escape, abort, flash, send_from_directory
import sys, requests, json
from dbconnect import connection
from wtforms import *
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import gc, string, random
from datetime import datetime


app = Flask (__name__)
app.secret_key = "Random String"

@app.route('/', methods = ['POST', 'GET'])
def home():
	if request.method == "POST":
		uniqueid = request.form['uniqueid']
		data = request.form['data']
		return render_template('main.html', data = data)
	return render_template ('main.html')

@app.route('/checkLogin/', methods = ['POST'])
def checkLogin():
	c, conn = connection()
	username = request.form['username']
	password = request.form['password']
	x = c.execute("select username from users where username = (%s)",(username,))
	if (c.fetchone() is not None):
		c.execute("select * from users where username = (%s) and password = (%s)",(username, password))
		if (c.fetchone() is not None):
			session["logged_in"] = True
			session["username"] = username
			return redirect(url_for('home'))
		else:
			flash("Password is incorrect!")
			return render_template('Login.html')
	flash("Please create an account first to login!")		
	return render_template('Login.html')			

@app.route('/login/')
def login():
	return render_template('Login.html')

@app.route('/logout/')
def logout():
	if session['logged_in'] and session['username']:
		session.pop('logged_in')
		session.pop('username')
	return redirect(url_for('home'))

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

	if session.get('logged_in') and session.get('username'):
		c, conn = connection()
		c.execute("select uid from users where username = (%s)", (session['username'],))
		userid = c.fetchone()[0]
		uniqueid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
		c.execute("insert into mycode (userid, createdon, data, uniqueid) values (%s,%s,%s,%s)", (userid, thwart(str(datetime.now())), thwart(str(source)), uniqueid))
		conn.commit()

	return render_template('main.html', Result = json.loads(response.text))

class RegistrationForm(Form):
	username = TextField('Username', [validators.Length(min = 4, max = 20)])
	email = TextField('Email', [validators.Length(min = 4, max = 50)])
	password = PasswordField('Password', [validators.Required(), validators.EqualTo('confirm', message = "Passwords don't match!")])
	confirm = PasswordField('Repeat Password')
	accept_tos = BooleanField('I accept the <a href="/tos/">Terms of service</a> and the <a href = "/privacy/"privacy notice</a> (Last updated Jul 2 2018)', [validators.required()])

@app.route('/register/', methods = ['GET', 'POST'])
def register_page():
	try:
		form = RegistrationForm(request.form)

		if request.method == "POST" and form.validate():
			username = form.username.data
			email = form.email.data
			password = str(form.password.data)
			c, conn = connection()

			x = c.execute("select * from users where username = (%s)",(username,))
			
			if (c.fetchone() is not None):
				flash ("The username already exists! Please choose a different username.")
				return render_template("register.html", form = form)

			else:
				c.execute ("insert into users (username, password, email) values (%s,%s,%s)", (thwart(username), thwart(password), thwart(email)))			
				conn.commit()

				flash("Thanks for registering!")

				c.close()
				conn.close()

				gc.collect()

				session["logged_in"] = True
				session["username"] = username

				return redirect(url_for('home'))

		return render_template("register.html", form = form)

	except Exception as e:
		return (str(e))	

@app.route('/PreviousCodes/')
def previousCodes():
	c, conn = connection()
	c.execute("select * from users where username = (%s)", (session['username'],))
	userid = c.fetchone()[0]
	c.execute("select * from mycode where userid = (%s)",(userid,))
	previous_codes_list = c.fetchall()
	return render_template('previouscodes.html', list = previous_codes_list)


if __name__== '__main__':
	app.run(debug = True)