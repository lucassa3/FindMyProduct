from flask import Flask, render_template, request, flash, redirect, session
from werkzeug import generate_password_hash, check_password_hash
from ConnectionHelper import ConnectionHelper

app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'


db = ConnectionHelper()

@app.route("/",methods=['POST','GET'])
def main():
	return render_template('index.html')



@app.route("/validateLogin",methods=['POST'])
def validateLogin():
	email = request.form['email']
	senha = request.form['senha']

	pass_check = db.run("select senha from usuario where email='"+email+"';")

	if check_password_hash(pass_check[0], senha):
		user_log = db.run("select usuario_id from usuario where email='"+email+"';")
		session['user'] = user_log[0]
		return redirect('/userHome')
	else:
 		return "USUARIO NÃO ENCONTRADO"



@app.route("/userHome")
def userHome():
	if session.get('user'):
		return render_template('userHome.html')
	else:
		return "ACESSO NÃO AUTORIZADO!"



@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')



@app.route("/register",methods=['POST','GET'])
def register():
	return render_template('register.html')



@app.route("/validateRegister" , methods=['POST'])
def validateRegister():
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

		else:
			return "as senhas nao batem!"


if __name__ == "__main__":
	app.run()