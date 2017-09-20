from flask import Flask, render_template, request, flash, redirect, session, json, jsonify, url_for
from DAO import DAO
import requests
import uuid
import os

app = Flask(__name__)
app.secret_key = '123456'


<<<<<<< HEAD

=======
>>>>>>> 3df1bc1708b12c2db9a52dcdfe36be5262fb01bb
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
		flash('USUÁRIO E/OU SENHA INVÁLIDOS')
		return redirect('/')



@app.route("/userHome", methods=['GET'])
def userHome():
	if session.get('user'):
		username = dao.getUserFromId(str(session.get('user')))

		brand_list = []

		return render_template('userHome.html', username=username,brand_list=brand_list)
	
	else:
		return redirect('/')



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
				flash('AS SENHAS NÃO COINCIDEM!')
				return redirect('/userRegister')
		
		else:
			flash('EMAIL JÁ CADASTRADO!')
			return redirect('/userRegister')



@app.route('/userInfo')
def userInfo():
	if session.get('user'):
		username = dao.getUserFromId(str(session.get('user')))
		lastname = dao.getLastNameFromId(str(session.get('user')))
		email = dao.getEmailFromId(str(session.get('user')))
		birth_date = dao.getBirthDateFromId(str(session.get('user')))
		gender = dao.getGenderFromId(str(session.get('user')))
		password = dao.getPasswordFromId(str(session.get('user')))

		return render_template("userInfo.html",username=username,lastname=lastname,email=email,birth_date=birth_date,gender=gender)

	else:
		return redirect("/")


@app.route('/userEdit', methods=['GET','POST'])
def editUserInfo():
	if session.get('user'):
		username = dao.getUserFromId(str(session.get('user')))
		lastname = dao.getLastNameFromId(str(session.get('user')))
		email = dao.getEmailFromId(str(session.get('user')))
		birth_date = dao.getBirthDateFromId(str(session.get('user')))
		gender = dao.getGenderFromId(str(session.get('user')))

		return render_template("userEdit.html", username=username,lastname=lastname,email=email,birth_date=birth_date,gender=gender)

	else:
		return redirect("/")



@app.route('/validateUserEdit', methods=['POST'])
def validateUserEdit():
	if request.method == 'POST':
		name = request.form['name']
		lastname = request.form['lastname']
		gender = request.form['gender']
		email = request.form['email']
		birth_date = request.form['birth_date']

		current_email = dao.getEmailFromId(str(session.get('user')))
		
		email_check = dao.isUserEmailAlreadyRegistered(email)

		if current_email == email or email_check == False:


			dao.editUser(str(session.get('user')),name,lastname,email,birth_date,gender)
			return redirect('/userInfo')

		else:
			flash('EMAIL JÁ CADASTRADO!')
			return redirect('/userEdit')



@app.route('/userEditPassword', methods=['GET','POST'])
def userEditPassword():
	if session.get('user'):
		username = dao.getUserFromId(str(session.get('user')))
		return render_template('userEditPassword.html',username=username)
	else:
		return redirect("/")




@app.route('/validateUserEditPassword', methods=['POST'])
def validateUserEditPassword():
	if request.method == 'POST':

		password = request.form['password']
		check_password = request.form['check_password']

		if password == check_password:
			dao.editUserPassword(str(session.get('user')),password)

			return redirect('/userInfo')

		else:
			flash("AS SENHAS NÃO COINCIDEM!")
			return redirect('/userEditPassword')



@app.route('/userLogout')
def logout():
    session.pop('user', None)
   
    return redirect('/')



@app.route("/userHome/search", methods=['POST'])
def userSearch():
	if session.get('user'):
		search = request.form['search']
		lat = request.form['latitude']
		lng = request.form['longitude']
		checkbox = request.form['radio']

		lat1 = ""
		lng1 = ""

		brand_list = dao.listBrand(search)		
		
		if checkbox == "none":
			result = dao.searchProduct(search)
			soldout = dao.searchSoldOut(search)
		else:
			result = dao.searchProductByBrand(search,checkbox)
			soldout = dao.searchSoldOutByBrand(search,checkbox)

		username = dao.getUserFromId(str(session.get('user')))
		
		distances = []

		for i in result:
			lat1 = i[4]
			lng1 = i[5]

			distances.append(round(dao.distance(float(lat),float(lng),float(lat1),float(lng1)), 2))

		if result or soldout:

			return render_template('userHome.html', result=result, username=username, distances=distances, brand_list=brand_list,soldout=soldout)

		else:
			flash('NENHUM PRODUTO ENCONTRADO')
			return redirect('/userHome')

	else:
		return redirect("/")
		



@app.route("/product", methods=['POST'])
def product():
	if request.method == 'POST':
		if session.get('user'):
			product_id = request.form['id']
			distance = request.form['distance']
			
			
			product = dao.getProductById(product_id)


			username = dao.getUserFromId(str(session.get('user')));
			return render_template('product.html', product=product, username=username, distance=distance)
		else:
			return redirect("/")

@app.route("/validateBuy", methods=['POST'])
def validateBuy():
	if request.method == 'POST':
		if session.get('user'):
			product_id = request.form['product_id']
			username_id = str(session.get('user'))
			date = request.form['date']
			quantity = request.form['quantity']

			dao.userBuyProduct(date, username_id, product_id, quantity)
			username = dao.getUserFromId(str(session.get('user')));

			return render_template('productPurchased.html', username=username)

		else:
			return redirect("/")


###############################STORE-ROUTES########################################



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
		flash("USUARIO E/OU SENHA INVÁLIDOS!")
		return redirect('/storeSignIn')


@app.route("/storeHome")
def storeHome():
	if session.get('store'):
		storename = dao.getStoreNameFromId(str(session.get('store')));
		lista_compras = dao.listCompras(storename)
		print(lista_compras)
		
		return render_template('storeHome.html', storename=storename)
	else:
		return redirect('/storeSignIn')


@app.route("/storeProducts")
def storeProducts():
	if session.get('store'):
		storename = dao.getStoreNameFromId(str(session.get('store')));
		products = dao.getStoreProducts(str(session.get('store')))
		return render_template('storeProducts.html', storename=storename, products=products)
	else:
		return redirect('/storeSignIn')

@app.route("/getProductById", methods=['POST'])
def getProductById():
	if session.get('store'):
		product_id = request.form['id']
		storename = dao.getStoreNameFromId(str(session.get('store')))
		product = dao.getProductById(product_id)


		product_list = []
		product_list.append({'produto_id':product[0][0],'preco': str(product[0][1]),'marca':product[0][2],'nome':product[0][3],'descricao':product[0][5],'quantidade':product[0][6]})

		return json.dumps(product_list)

	else:
		return redirect('/storeSignIn')

@app.route("/updateProduct", methods=['POST'])
def updateProduct():
	if session.get('store'):
		product_id = request.form['product_id']
		name = request.form['name']
		brand = request.form['brand']
		price = request.form['price']
		stock = request.form['stock']
		description = request.form['description']

		dao.editProduct(product_id, name, brand, price, description, stock)
		
		return json.dumps({'status':'OK'})

	else:
		return redirect('/storeSignIn')


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

		address_init = "https://maps.googleapis.com/maps/api/geocode/json?address="
		api_key = "&key=AIzaSyDsHltt99bw8drFOi4wUqdYJ3LQO4tWZh8"

		address_list = str(address).split()
		print(address_list)
		address_for_url = ""

		for i in address_list:
			address_for_url += str(i) + "+"

		address_for_url = address_for_url[:-1]
		print(address_for_url)

		final_address = address_init + address_for_url + api_key
		print(final_address)
		address_info = requests.get(final_address).json()
		print(address_info["results"])
		
		lat = ""
		lng = ""

		for i in address_info["results"]:
			lat = str(i["geometry"]["location"]["lat"])
			lng = str(i["geometry"]["location"]["lng"])

<<<<<<< HEAD



=======
>>>>>>> 3df1bc1708b12c2db9a52dcdfe36be5262fb01bb
		email_check = dao.isStoreEmailAlreadyRegistered(email)
		if email_check == False:
			if password == check_password:
				dao.validateStoreRegister(name, telephone, address, email, password, lat, lng)
				return redirect("/storeSignIn")
			else:
				flash("AS SENHAS NÃO COINCIDEM!")
				return redirect("/storeRegister")
		else:
			flash("EMAIL JÁ CADASTRADO!")
			return redirect("/storeRegister")

@app.route('/addProduct')
def addProduct():
	if session.get('store'):
		storename = dao.getStoreNameFromId(str(session.get('store')));
		return render_template('/addProduct.html', storename=storename)
	else:
		return redirect('/storeSignIn')

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
		description = request.form['description']

		if request.form.get('filePath') is None:
			filePath = ''
		else:
			filePath = request.form.get('filePath')

		dao.storeAddProduct(name, brand, price, stock, filePath, description, session.get('store'))
		return redirect('/storeHome')


@app.route('/storeLogout')
def storeLogout():
    session.pop('store', None)
    return redirect('/storeSignIn')



@app.route('/storeInfo')
def storeInfo():

	if session.get('store'):
		address = dao.getAddressFromId(str(session.get('store')));
		phone = dao.getPhoneFromId(str(session.get('store')));
		storename = dao.getStoreNameFromId(str(session.get('store')));
		email = dao.getStoreEmailFromId(str(session.get('store')));

		return render_template("storeInfo.html",address=address,phone=phone,storename=storename,email=email)
	else:
		return redirect('/storeSignIn')

@app.route('/storeEdit',methods=['GET','POST'])
def storeEdit():

	if session.get('store'):
		address = dao.getAddressFromId(str(session.get('store')));
		phone = dao.getPhoneFromId(str(session.get('store')));
		storename = dao.getStoreNameFromId(str(session.get('store')));
		email = dao.getStoreEmailFromId(str(session.get('store')));

		return render_template("storeEdit.html",address=address,phone=phone,storename=storename,email=email)
	else:
		return redirect('/storeSignIn')

@app.route('/validateStoreEdit', methods=['POST'])
def validateStoreEdit():

	if request.method == 'POST':

		storename = request.form['storename']
		email = request.form['email']
		phone = request.form['phone']
		address = request.form['address']

		current_email = dao.getStoreEmailFromId(str(session.get('store')));
		email_check = dao.isStoreEmailAlreadyRegistered(email)

		if current_email == email or email_check == False:
			dao.editStore(str(session.get('store')),address,phone,storename,email)
			return redirect('/storeInfo')

		else:
			flash("EMAIL JÁ CADASTRADO!")
			return redirect('/storeEdit')


@app.route('/storeEditPassword', methods=['GET','POST'])
def userStorePassword():
	if session.get('store'):
		storename = dao.getStoreNameFromId(str(session.get('store')));
		return render_template('storeEditPassword.html',storename=storename)
	else:
		return redirect('/storeSignIn')

@app.route('/validateStoreEditPassword', methods=['POST'])
def validateStoreEditPassword():

	if request.method == 'POST':

		password = request.form['password']
		check_password = request.form['check_password']

		if password == check_password:

			dao.editStorePassword(str(session.get('store')),password)

			return redirect('/storeInfo')

		else:
			flash("AS SENHAS NÃO COINCIDEM!")
			return redirect('/storeEditPassword')

if __name__ == "__main__":
	app.run()