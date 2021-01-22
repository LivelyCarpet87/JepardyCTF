from serverBackend import data
import sqlite3,time
import string, random

def panel3(user,pwd):
	command = "SELECT * FROM logins WHERE username ='" + user + "' AND password ='" + pwd + "'"
	db = sqlite3.connect(":memory:")
	db.create_function("SLEEP", 1, time.sleep)
	db.create_function("WAITFOR", 1, time.sleep)
	c = db.cursor()

	filter = data.getOtherData("loginPanels","panel3")["filter"]

	c.execute("CREATE TABLE logins (username text, password text)")
	adminPassword = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
	c.execute("INSERT INTO logins VALUES (?,?)",("admin",adminPassword))
	db.commit()
	c = db.cursor()
	try:
		x = c.execute(command)
		account = x.fetchone()
		if account:
			message = "Login Success."
		else:
			message = "Login Failed."
	except sqlite3.Warning as w:
		message = "Warning: "+repr(w.args[0])
	except sqlite3.Error as e:
		message = "Error: "+repr(e.args[0])
	db.rollback()
	db.close()
	return (message == "Login Success."), command, message

name="panel3"
