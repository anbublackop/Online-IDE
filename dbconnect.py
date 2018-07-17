import MySQLdb

def connection():
	conn = MySQLdb.connect(host='us-cdbr-iron-east-04.cleardb.net', user = 'b50f908f898101', passwd = '42c7163a', db = 'heroku_fa7e2ebc29221a0')
	c = conn.cursor()
	return c, conn
