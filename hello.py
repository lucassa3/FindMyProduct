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
    'database': 'fmp',
	'autocommit':True    
}

connection = pymysql.connect(**connection_options)

db = ConnectionHelper(connection)

@app.route("/",methods=['POST','GET'])

def main():

	if request.method == 'POST':

	 	email = request.form['email']
	 	senha = request.form['senha']

	 	pass_check = db.run("select senha from usuario where email='"+email+"';")

	 	if pass_check[0] == senha:

	 		return "LOGIN EFETUADO"
	 	else:
	 		return "USUARIO NÃO ENCONTRADO"

	return render_template('index.html')

@app.route("/register",methods=['POST','GET'])

def register():

	if request.method == 'POST':
		nome = request.form['nome']
		sobrenome = request.form['sobrenome']
		sexo = request.form['sexo']
		email = request.form['email']
		senha = request.form['senha']
		confirma_senha = request.form['confirma_senha']
		
		
		


		if senha == confirma_senha:
			db.run("insert into usuario(nome,sobrenome,sexo,email,senha) VALUES('"+nome+"','"+sobrenome+"','"+sexo+"','"+email+"','"+senha+"');")

			return redirect("/")

			#print("email:"+ email + "\nNome: " + name)
		else:
			print("as senhas não batem")

	return render_template('register.html')

if __name__ == "__main__":
	app.run()