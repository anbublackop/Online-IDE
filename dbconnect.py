import MySQLdb

def connection():
	conn = MySQLdb.connect(host='localhost', user = 'root', passwd = 'hashirama', db = 'Online_IDE')
	c = conn.cursor()
	return c, conn
