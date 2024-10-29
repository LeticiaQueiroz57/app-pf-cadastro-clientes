import pymongo 

url_database = 'mongodb+srv://m0:root@cluster0.hqp4qrc.mongodb.net/'

banco = pymongo.MongoClient(url_database)

db = banco['Grupo_1']

Patient = db.Patient
Usuario =  db.Usuarios
Produto = db.Produto


