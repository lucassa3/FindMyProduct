# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, flash, redirect
import pymysql
import os

app = Flask(__name__)

#Read Credentials from file
file = open("credential.txt","r")
entrada = []
with open ("credential.txt", "r") as myfile:
    for line in myfile:
        entrada.append(line)

mysql_user = entrada[0].strip()
mysql_password = entrada[1].strip()

#MySQL connection
class ConnectionHelper:
    def __init__(self, connection):
        self.connection = connection
    
    def run(self, query, args=None):
        with self.connection.cursor() as cursor:
            print('Executando query:')
            print(cursor.mogrify(query, args))
            cursor.execute(query, args)
            for result in cursor.fetchall():
            	print(result)
            	return(result)

connection_options = {
    'host': 'localhost',
    'user': mysql_user,
    'password': mysql_password,
    'database': 'FindMyStuff',
	'autocommit':True    
}

connection = pymysql.connect(**connection_options)

db = ConnectionHelper(connection)

@app.route("/",methods=['POST','GET'])

def main():

	if request.method == 'POST':

	 	email = request.form['user']
	 	password = request.form['password']

	 	pass_check = db.run("select password from user where email='"+email+"';")

	 	if pass_check[0] == password:

	 		return "LOGIN EFETUADO"
	 	else:
	 		return "USUARIO NÃO ENCONTRADO"

	return render_template('index.html')

@app.route("/register",methods=['POST','GET'])

def register():

	if request.method == 'POST':

		email = request.form['user']
		password = request.form['password']
		confirm_password = request.form['confirm_password']
		name = request.form['name']

		if password == confirm_password:
			db.run("insert into user(email,name,password) VALUES('"+email+"','"+name+"','"+password+"');")

			return redirect("/")

			#print("email:"+ email + "\nNome: " + name)
		else:
			print("as senhas não batem")

	return render_template('register.html')

if __name__ == "__main__":
	app.run()