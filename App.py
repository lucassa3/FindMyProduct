from flask import Flask, render_template, request, flash, redirect, session
from werkzeug import generate_password_hash, check_password_hash
from ConnectionHelper import ConnectionHelper
from DAO import DAO

app = Flask(__name__)
app.secret_key = '123456'

dao = DAO()

@app.route("/")
def main():
	return render_template('index.html')


@app.route("/validateLogin", methods=['POST'])
def validateLogin():
	email = request.form['email']
	password = request.form['password']

	pass_check = dao.validateUserPassword(email, password)

	if pass_check:
		session['user'] = pass_check
		return redirect('/userHome')
	else:
 		return "USUARIO E/OU SENHA NÃO ENCONTRADOS"


@app.route("/userHome")
def userHome():
	if session.get('user'):
		return render_template('userHome.html')
	else:
		return "ACESSO NÃO AUTORIZADO!"


@app.route("/userRegister")
def register():
	return render_template('userRegister.html')


@app.route("/validateUserRegister", methods=['POST'])
def validateRegister():
	if request.method == 'POST':
		name = request.form['name']
		lastname = request.form['lastname']
		gender = request.form['gender']
		email = request.form['email']
		birth_date = request.form['birth_date']
		password = request.form['password']
		check_password = request.form['check_password']

		if password == check_password:
			dao.validateUserRegister(name, lastname, gender, email, password, birth_date)
			return redirect("/")
		else:
			return "as senhas nao batem!"


@app.route('/userLogout')
def logout():
    session.pop('user', None)
    return redirect('/')






@app.route("/storeSignIn")
def storeSignIn():
		return render_template('storeSignIn.html')


@app.route("/validateStoreLogin", methods=['POST'])
def validateStoreLogin():
	email = request.form['email']
	password = request.form['password']

	pass_check = dao.validateStorePassword(email, password)
	if pass_check:
		session['store'] = pass_check
		return redirect('/storeHome')
	else:
		return "USUARIO E/OU SENHA NÃO ENCONTRADOS"


@app.route("/storeHome")
def StoreHome():
	if session.get('store'):
		return render_template('storeHome.html')
	else:
		return "ACESSO NÃO AUTORIZADO!"


@app.route("/storeRegister")
def storeRegister():
	return render_template('storeRegister.html')


@app.route("/validateStoreRegister", methods=['POST'])
def validateStoreRegister():
	if request.method == 'POST':
		name = request.form['name']
		telephone = request.form['telephone']
		address = request.form['address']
		email = request.form['email']
		password = request.form['password']
		check_password = request.form['check_password']

		if password == check_password:
			dao.validateStoreRegister(name, telephone, address, email, password)
			return redirect("/storeSignIn")
		else:
			return "as senhas nao batem!"


@app.route('/addProduct')
def addProduct():
	if session.get('store'):
		return render_template('/addProduct.html')
	else:
		return "acesso nao autorizado!"


@app.route('/validateProduct', methods=['POST'])
def validateProduct():
	if request.method == 'POST':
		name = request.form['name']
		brand = request.form['brand']
		price = request.form['price']

		dao.storeAddProduct(name, brand, price)
		return "produto adicionado!"


@app.route('/storeLogout')
def storeLogout():
    session.pop('store', None)
    return redirect('/storeSignIn')








if __name__ == "__main__":
	app.run()