from werkzeug import generate_password_hash, check_password_hash
from ConnectionHelper import ConnectionHelper


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

	#####################################################################################


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

		
	def validateStoreRegister(self, name, telephone, address, email, password):
		hash_pass = generate_password_hash(password)
		self.db.run("insert into loja(nome,telefone,endereco,email,senha) VALUES('"+name+"','"+telephone+"','"+address+"','"+email+"','"+hash_pass+"');")

	def storeAddProduct(self, name, brand, price, stock, filePath, store_id):
		self.db.run("insert into produto(nome,marca,preco, quantidade, path_foto, loja_loja_id) VALUES('"+name+"','"+brand+"','"+price+"','"+stock+"','"+filePath+"','"+str(store_id)+"');")

	def getStoreNameFromId(self, store_id):
		storename = self.db.run("select nome from loja where loja_id='"+store_id+"';")
		return str(storename[0][0])
	
	def searchProduct(self, name):
		result = self.db.run("select nome, preco, path_foto, produto_id from produto where nome like '%"+name+"%';")
		return result

	def getProductById(self, product_id):
		result = self.db.run("select * from produto where produto_id='"+product_id+"';")
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

	def editUserPassword(self, user_id, password):
		hash_pass = generate_password_hash(password)
		self.db.run("update usuario set senha='"+hash_pass+"' where usuario_id='"+user_id+"';")