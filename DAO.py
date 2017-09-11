from werkzeug import generate_password_hash, check_password_hash
from ConnectionHelper import ConnectionHelper


class DAO:

	def __init__(self):
		self.oi = 0
		self.db = ConnectionHelper()

	def validateUserPassword(self, email, password):
		pass_check = self.db.run("select senha from usuario where email='"+email+"';")
		
		if pass_check[0][0]:
			if check_password_hash(pass_check[0][0], password):
				user_log = self.db.run("select usuario_id from usuario where email='"+email+"';")
				return user_log[0][0]
		return False


	def validateStorePassword(self, email, password):
		pass_check = self.db.run("select senha from loja where email='"+email+"';")
		
		if pass_check[0][0]:
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

	def storeAddProduct(self, name, brand, price, stock, store_id):
		self.db.run("insert into produto(nome,marca,preco, quantidade, loja_loja_id) VALUES('"+name+"','"+brand+"','"+price+"','"+stock+"','"+str(store_id)+"');")

	def getUserFromId(self, user_id):
		username = self.db.run("select nome from usuario where usuario_id='"+user_id+"';")
		return str(username[0][0])
	
	def searchProduct(self, name):
		result = self.db.run("select nome, preco from produto where nome like '%"+name+"%';")
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



		

		









