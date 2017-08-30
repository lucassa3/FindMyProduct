# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, flash


app = Flask(__name__)

"""
mysql = MySQL()

app.config['MYSQL_DATABSE_USER'] = 'root'
app.config['MYSQL_DATABSE_PASSWORD'] = 'toyama'
app.config['MYSQL_DATABSE_DB'] = 'FindMyStuff'
app.config['MYSQL_DATABSE_HOST'] = 'localhost'
mysql.init_app(app)
"""

@app.route("/",methods=['POST','GET'])	

def main():

	if request.method == 'POST':

	 	   email = request.form['user']
	 	   password = request.form['password']

	 	   print(email + " " + password)

	return render_template('index.html')

@app.route("/register",methods=['POST','GET'])

def register():

	if request.method == 'POST':

		email = request.form['user']
		password = request.form['password']
		confirm_password = request.form['confirm_password']
		name = request.form['name']

		if password == confirm_password:

			print("email:"+ email + "\nNome: " + name)
		else:
			print("as senhas não batem")

	return render_template('register.html')


if __name__ == "__main__":
	app.run()