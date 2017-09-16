from flask import Flask, render_template, request, flash, redirect, session, json, jsonify, url_for
from DAO import DAO
import uuid
import os

app = Flask(__name__)
app.secret_key = '123456'

dao = DAO()

app.config['UPLOAD_FOLDER'] = 'static/Uploads'

@app.route("/")
def main():
	if session.get('user'):
		return redirect('/userHome')
	
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


@app.route("/userHome", methods=['GET'])
def userHome():
	if session.get('user'):
		username = dao.getUserFromId(str(session.get('user')))
		return render_template('userHome.html', username=username)
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

		email_check = dao.isUserEmailAlreadyRegistered(email)
		if email_check == False:
			if password == check_password:
				dao.validateUserRegister(name, lastname, gender, email, password, birth_date)
				return redirect("/")
			else:
				return "as senhas nao coincidem!"
		else:
			return "email ja escolhido!"


@app.route('/userLogout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route("/userHome/search", methods=['POST'])
def userSearch():
	if session.get('user'):
		search = request.form['search']
		result = dao.searchProduct(search)
		username = dao.getUserFromId(str(session.get('user')))
		print(result)
		if result:
			return render_template('userHome.html', result=result, username=username)
		else:
			return "nenhum produto encontrado!"






@app.route("/storeSignIn")
def storeSignIn():
	if session.get('store'):
		return redirect('/storeHome')
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
		storename = dao.getStoreNameFromId(str(session.get('store')));
		return render_template('storeHome.html', storename=storename)
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

		email_check = dao.isStoreEmailAlreadyRegistered(email)
		if email_check == False:
			if password == check_password:
				dao.validateStoreRegister(name, telephone, address, email, password)
				return redirect("/storeSignIn")
			else:
				return "as senhas nao coincidem!"
		else:
			return "email ja escolhido!"


@app.route('/addProduct')
def addProduct():
	if session.get('store'):
		storename = dao.getStoreNameFromId(str(session.get('store')));
		return render_template('/addProduct.html',storename=storename)
	else:
		return "acesso nao autorizado!"

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		file = request.files['file']
		extension = os.path.splitext(file.filename)[1]
		print(extension)
		f_name = str(uuid.uuid4()) + extension
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
		return json.dumps({'filename':f_name})


@app.route('/validateProduct', methods=['POST'])
def validateProduct():
	if request.method == 'POST':
		name = request.form['name']
		brand = request.form['brand']
		price = request.form['price']
		stock = request.form['stock']

		if request.form.get('filePath') is None:
			filePath = ''
		else:
			filePath = request.form.get('filePath')

		dao.storeAddProduct(name, brand, price, stock, filePath, session.get('store'))
		return "produto adicionado!"


@app.route('/storeLogout')
def storeLogout():
    session.pop('store', None)
    return redirect('/storeSignIn')








if __name__ == "__main__":
	app.run()