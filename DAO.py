from werkzeug import generate_password_hash, check_password_hash
from ConnectionHelper import ConnectionHelper


class DAO:

	def __init__(self):
		self.oi = 0
		self.db = ConnectionHelper()

	def validateUserPassword(self, email, password):
		pass_check = self.db.run("select senha from usuario where email='"+email+"';")
		
		if pass_check:
			if check_password_hash(pass_check[0], password):
				user_log = self.db.run("select usuario_id from usuario where email='"+email+"';")
				return user_log

		return False


	def validateStorePassword(self, email, password):
		pass_check = self.db.run("select senha from loja where email='"+email+"';")
		
		if pass_check:
			if check_password_hash(pass_check[0], password):
				store_log = self.db.run("select loja_id from loja where email='"+email+"';")
				return store_log

		return False

	def validateUserRegister(self, name, lastname, gender, email, password, birth_date):
		hash_pass = generate_password_hash(password)
		self.db.run("insert into usuario(nome,sobrenome,sexo,email,senha,data_nasc) VALUES('"+name+"','"+lastname+"','"+gender+"','"+email+"','"+hash_pass+"','"+birth_date+"');")

		
	def validateStoreRegister(self, name, telephone, address, email, password):
		hash_pass = generate_password_hash(password)
		self.db.run("insert into loja(nome,telefone,endereco,email,senha) VALUES('"+name+"','"+telephone+"','"+address+"','"+email+"','"+hash_pass+"');")

	def storeAddProduct(self, name, brand, price):
		self.db.run("insert into produto(nome,marca,preco) VALUES('"+name+"','"+brand+"','"+price+"');")
	

		

		









