from werkzeug import generate_password_hash, check_password_hash
from ConnectionHelper import ConnectionHelper
from math import cos, asin, sqrt


class DAO:

	def __init__(self):
		self.oi = 0
		self.db = ConnectionHelper()

	#GET USER
	def getUserFromId(self, user_id):
		username = self.db.run("select nome from usuario where usuario_id='"+user_id+"';")
		return str(username[0][0])

	def getLastNameFromId(self, user_id):
		lastname = self.db.run("select sobrenome from usuario where usuario_id='"+user_id+"';")
		return str(lastname[0][0])

	def getEmailFromId(self, user_id):
		email = self.db.run("select email from usuario where usuario_id='"+user_id+"';")
		return str(email[0][0])

	def getBirthDateFromId(self, user_id):
		birth_date = self.db.run("select data_nasc from usuario where usuario_id='"+user_id+"';")
		return str(birth_date[0][0])

	def getGenderFromId(self, user_id):
		gender = self.db.run("select sexo from usuario where usuario_id='"+user_id+"';")
		return str(gender[0][0])

	def getPasswordFromId(self, user_id):
		password = self.db.run("select senha from usuario where usuario_id='"+user_id+"';")
		return str(password[0][0])

#########################################################################################

	#GET STORE

	def getAddressFromId(self,store_id):
		address = self.db.run("select endereco from loja where loja_id='"+store_id+"';")
		return str(address[0][0])

	def getPhoneFromId(self,store_id):
		phone = self.db.run("select telefone from loja where loja_id='"+store_id+"';")
		return str(phone[0][0])

	def getStoreNameFromId(self, store_id):
		storename = self.db.run("select nome from loja where loja_id='"+store_id+"';")
		return str(storename[0][0])

	def getStoreEmailFromId(self,store_id):
		email = self.db.run("select email from loja where loja_id='"+store_id+"';")
		return str(email[0][0])

	def getStorePasswordFromId(self,store_id):
		password = self.db.run("select senha from loja where loja_id='"+store_id+"';")
		return str(password[0][0])

#########################################################################################

	def validateUserPassword(self, email, password):
		pass_check = self.db.run("select senha from usuario where email='"+email+"';")
		
		if pass_check:
			if check_password_hash(pass_check[0][0], password):
				user_log = self.db.run("select usuario_id from usuario where email='"+email+"';")
				return user_log[0][0]
		return False


	def validateStorePassword(self, email, password):
		pass_check = self.db.run("select senha from loja where email='"+email+"';")
		
		if pass_check:
			if check_password_hash(pass_check[0][0], password):
				store_log = self.db.run("select loja_id from loja where email='"+email+"';")
				return store_log[0][0]
		return False

	def validateUserRegister(self, name, lastname, gender, email, password, birth_date):
		hash_pass = generate_password_hash(password)
		self.db.run("insert into usuario(nome,sobrenome,sexo,email,senha,data_nasc) VALUES('"+name+"','"+lastname+"','"+gender+"','"+email+"','"+hash_pass+"','"+birth_date+"');")

		
	def validateStoreRegister(self, name, telephone, address, email, password, lat, lng):
		hash_pass = generate_password_hash(password)
		self.db.run("insert into loja(nome,telefone,endereco,email,senha,latitude,longitude) VALUES('"+name+"','"+telephone+"','"+address+"','"+email+"','"+hash_pass+"','"+lat+"','"+lng+"');")

	def storeAddProduct(self, name, brand, price, stock, filePath, description, store_id):
		self.db.run("insert into produto(nome,marca,preco, quantidade, path_foto, descricao, loja_loja_id) VALUES('"+name+"','"+brand+"','"+price+"','"+stock+"','"+filePath+"','"+description+"','"+str(store_id)+"');")
	
	def searchProduct(self, name):
		result = self.db.run("select p.nome, p.preco, path_foto, produto_id, latitude, longitude from produto p, loja l where p.loja_loja_id = l.loja_id and p.nome like '%"+name+"%' and p.quantidade > 0;")
		return result

	def searchProductByBrand(self, name, brand):
		result = self.db.run("select p.nome, p.preco, path_foto, produto_id, latitude, longitude from produto p, loja l where p.loja_loja_id = l.loja_id and marca='"+brand+"' and p.nome like '%"+name+"%' and p.quantidade > 0;")
		return result

	def searchSoldOut(self, name):
		result = self.db.run("select p.nome, p.preco, path_foto, produto_id, latitude, longitude from produto p, loja l where p.loja_loja_id = l.loja_id and p.nome like '%"+name+"%' and p.quantidade = 0;")
		return result

	def userBuyProduct(self, purchase_date, user_id, product_id, quantity):
		self.db.run("insert into compra(data_compra, usuario_usuario_id, produto_produto_id, quantidade) VALUES('"+purchase_date+"','"+user_id+"','"+product_id+"','"+quantity+"');")
		self.db.run("update produto set quantidade= quantidade - "+quantity+" where produto_id='"+product_id+"';")


	def getProductById(self, product_id):
		result = self.db.run("select * from produto p, loja l where p.loja_loja_id = l.loja_id and produto_id='"+product_id+"';")
		return result

	def getStoreProducts(self, store_id):
		result = self.db.callproc('get_store_products',(store_id))
		#result = self.db.run("call get_store_products ('"+store_id+"');")
		return result

	def isUserEmailAlreadyRegistered(self, email):
		result = self.db.run("select email from usuario where email = '"+email+"';")
		if result:
			return True
		else:
			return False

	def isStoreEmailAlreadyRegistered(self, email):
		result = self.db.run("select email from loja where email = '"+email+"';")
		if result:
			return True
		else:
			return False

	def editUser(self, user_id, name, lastname, email, birth_date, gender):
		self.db.run("update usuario set nome='"+name+"', sobrenome='"+lastname+"',email='"+email+"', data_nasc='"+birth_date+"',sexo='"+gender+"' where usuario_id='"+user_id+"';")

	def editProduct(self, product_id, name, brand, price, description, stock):
		self.db.run("update produto set nome='"+name+"', marca='"+brand+"', preco='"+price+"', descricao='"+description+"',quantidade='"+stock+"' where produto_id='"+product_id+"';")

	def editUserPassword(self, user_id, password):
		hash_pass = generate_password_hash(password)
		self.db.run("update usuario set senha='"+hash_pass+"' where usuario_id='"+user_id+"';")
	
	def editStore(self, store_id, address, phone, storename, email):
		self.db.run("update loja set endereco='"+address+"', telefone='"+phone+"',nome='"+storename+"',email='"+email+"' where loja_id='"+store_id+"';")

	def editStorePassword(self, store_id, password):
		hash_pass = generate_password_hash(password)
		self.db.run("update loja set senha='"+hash_pass+"' where loja_id='"+store_id+"';")

	def distance(self, lat1, lon1, lat2, lon2):
		p = 0.017453292519943295 
		a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
		distance = 12742 * asin(sqrt(a)) 
		return distance #Km

	def deleteProduct(self, product_id):
		self.db.run("delete from produto where produto_id = '"+product_id+"';")


	def listBrand(self, name):
		brand_list = self.db.run("select distinct marca from produto where nome like '%"+name+"%';")
		return brand_list

