# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, flash, redirect
from werkzeug import generate_password_hash, check_password_hash
from ConnectionHelper import ConnectionHelper




app = Flask(__name__)



db = ConnectionHelper()

@app.route("/",methods=['POST','GET'])

def main():

	if request.method == 'POST':

	 	email = request.form['email']
	 	senha = request.form['senha']

	 	pass_check = db.run("select senha from usuario where email='"+email+"';")



	 	if check_password_hash(pass_check[0], senha):
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
		senha_hash = generate_password_hash(senha)
		confirma_senha = request.form['confirma_senha']
		
		
		


		if senha == confirma_senha:
			db.run("insert into usuario(nome,sobrenome,sexo,email,senha) VALUES('"+nome+"','"+sobrenome+"','"+sexo+"','"+email+"','"+senha_hash+"');")

			return redirect("/")

			#print("email:"+ email + "\nNome: " + name)
		else:
			print("as senhas não batem")

	return render_template('register.html')

if __name__ == "__main__":
	app.run()