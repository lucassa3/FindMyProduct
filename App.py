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
	if pass_check:
		if check_password_hash(pass_check[0], senha):
			user_log = db.run("select usuario_id from usuario where email='"+email+"';")
			session['user'] = user_log[0]
			return redirect('/userHome')
		else:
			return "USUARIO E/OU SENHA NÃO ENCONTRADOS"
	else:
 		return "USUARIO E/OU SENHA NÃO ENCONTRADOS"



@app.route("/userHome")
def userHome():
	if session.get('user'):
		return render_template('userHome.html')
	else:
		return "ACESSO NÃO AUTORIZADO!"

@app.route("/storeHome")
def StoreHome():
	if session.get('store'):
		return render_template('storeHome.html')
	else:
		return "ACESSO NÃO AUTORIZADO!"

@app.route("/storeSignIn")
def storeSignIn():
		return render_template('storeSignIn.html')

@app.route("/validateStoreLogin",methods=['POST'])
def validateStoreLogin():
	email = request.form['email']
	senha = request.form['senha']

	pass_check = db.run("select senha from loja where email='"+email+"';")
	if pass_check:
		if check_password_hash(pass_check[0], senha):
			user_log = db.run("select loja_id from loja where email='"+email+"';")
			session['store'] = user_log[0]
			return redirect('/storeHome')
		else:
			return "USUARIO E/OU SENHA NÃO ENCONTRADOS"
	else:
 		return "USUARIO E/OU SENHA NÃO ENCONTRADOS"




@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/storeLogout')
def storeLogout():
    session.pop('store', None)
    return redirect('/storeSignIn')

@app.route('/addProduct')
def addProduct():
	if session.get('store'):
		return render_template('/addProduct.html')
	else:
		return "acesso nao autorizado!"

@app.route('/validateProduct',methods=['POST','GET'])
def validateProduct():
	if request.method == 'POST':
		nome = request.form['nome']
		marca = request.form['marca']
		preco = request.form['preco']
		db.run("insert into produto(nome,marca,preco) VALUES('"+nome+"','"+marca+"','"+preco+"');")
		return "produto adicionado!"
	else:
		return "produto não adicionado!"



@app.route("/register",methods=['POST','GET'])
def register():
	return render_template('register.html')

@app.route("/storeRegister",methods=['POST','GET'])
def storeRegister():
	return render_template('storeRegister.html')



@app.route("/validateRegister" , methods=['POST'])
def validateRegister():
	if request.method == 'POST':
		nome = request.form['nome']
		sobrenome = request.form['sobrenome']
		sexo = request.form['sexo']
		email = request.form['email']
		data_nasc = request.form['data_nasc']
		senha = request.form['senha']
		senha_hash = generate_password_hash(senha)
		confirma_senha = request.form['confirma_senha']

		if senha == confirma_senha:
			db.run("insert into usuario(nome,sobrenome,sexo,email,senha,data_nasc) VALUES('"+nome+"','"+sobrenome+"','"+sexo+"','"+email+"','"+senha_hash+"','"+data_nasc+"');")

			return redirect("/")

		else:
			return "as senhas nao batem!"

@app.route("/validateStoreRegister" , methods=['POST'])
def validateStoreRegister():
	if request.method == 'POST':
		nome = request.form['nome']
		telefone = request.form['telefone']
		endereco = request.form['endereco']
		email = request.form['email']
		senha = request.form['senha']
		senha_hash = generate_password_hash(senha)
		confirma_senha = request.form['confirma_senha']

		if senha == confirma_senha:
			db.run("insert into loja(nome,telefone,endereco,email,senha) VALUES('"+nome+"','"+telefone+"','"+endereco+"','"+email+"','"+senha_hash+"');")

			return redirect("/storeSignIn")

		else:
			return "as senhas nao batem!"

if __name__ == "__main__":
	app.run()