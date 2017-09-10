import pymysql
import os

#MySQL connection
class ConnectionHelper:
    
    entrada = []
    
    def __init__(self):
        self.file = open("credential.txt","r")
        with open ("credential.txt", "r") as myfile:
            for line in myfile:
                self.entrada.append(line)

        self.mysql_user = self.entrada[0].strip()
        self.mysql_password = self.entrada[1].strip()

        self.connection_options = {
            'host': 'localhost',
            'user': self.mysql_user,
            'password': self.mysql_password,
            'database': 'fmp',
            'autocommit':True    
        }

        self.connection = pymysql.connect(**self.connection_options)
        
    def run(self, query, args=None):
        with self.connection.cursor() as cursor:
            print('Executando query:')
            print(cursor.mogrify(query, args))
            cursor.execute(query, args)
            for result in cursor.fetchall():
            	print(result)
            	return(result)

