import pymongo
import certifi

ca = certifi.where()
client = pymongo.MongoClient("mongodb+srv://usuario-pruebas:prueba123@cluster0.qfgmf.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=ca)

db = client.test
print(db)

baseDatos = client["bd-registro-academico"]
print(baseDatos.list_collection_names())