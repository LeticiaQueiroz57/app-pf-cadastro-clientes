import pymongo

url_database = ""

conexao = pymongo.MongoClient(url_database)

db = banco["db_hub"]

Usuario = db.Usuario

Produto = db.Produto





