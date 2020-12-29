from serverBackend import data

def panel1(user,pwd):
	command = "SELECT * FROM logins WHERE username ='" + user + "' AND password ='" + pwd + "'"
	db = sqlite3.connect(":memory:")
	db.create_function("SLEEP", 1, time.sleep)
	db.create_function("WAITFOR", 1, time.sleep)
	c = db.cursor()

	c.execute("CREATE TABLE logins (username text, password text)")
	c.execute("INSERT INTO logins VALUES (?,?)",("admin","password"))
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

name="panel1"

data.enrollChallenge("loginPanels",name,"N/A",
{
    "1": "Irish names."
},
50,{
    "filter":{}
})
