from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from flask_jwt_extended import create_access_token, verify_jwt_in_request, create_refresh_token, decode_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from waitress import serve
import datetime
import requests
import re

app=Flask(__name__)
app.config["JWT_SECRET_KEY"]="Secreto-proyecto-misiontic" #Cambiar por el que se
jwt = JWTManager(app)
cors = CORS(app)

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

@app.route("/login", methods=["POST"])
def create_token():
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url=dataConfig["url-backend-security"]+'/usuarios/validar'
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        user = response.json()
        expiresAccess = datetime.timedelta(seconds=60*5)
        expiresRefresh = datetime.timedelta(seconds=60 * 60*24)
        access_token = create_access_token(identity=user, expires_delta=expiresAccess)
        refresh_token = create_refresh_token(identity=user, expires_delta=expiresRefresh)
        return jsonify({"tokenAccess": access_token, "tokenRefresh":refresh_token, "user_id": user["_id"]})
    else:
        return jsonify({"msg": "Bad username or password"}), 401

@app.route("/",methods=['GET'])
def test():
    json = {}
    json["message"]="Server running ..."
    return jsonify(json)


@app.before_request
def before_request_callback():
    endPoint="/"+limpiarURL(request.path)
    excludedRoutes=["/login", "/refresh"]
    if excludedRoutes.__contains__(request.path):
        print("ruta excluida ",request.path)
        pass
    elif verify_jwt_in_request():
        usuario = get_jwt_identity()
        if usuario["rol"]is not None:
            tienePersmiso=validarPermiso(endPoint,request.method,usuario["rol"]["_id"])
            if not tienePersmiso:
                return jsonify({"message": "Permission denied"}), 401
        else:
            return jsonify({"message": "Permission denied"}), 401


##-------------Redireccionamiento estudiante----------##
@app.route("/estudiantes",methods=['GET'])
def getEstudiantes():
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/estudiantes'
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)
@app.route("/estudiantes",methods=['POST'])
def crearEstudiante():
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/estudiantes'
    response = requests.post(url, headers=headers,json=data)
    json = response.json()
    return jsonify(json)
@app.route("/estudiantes/<string:id>",methods=['GET'])
def getEstudiante(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/estudiantes/'+id
    response = requests.get(url, headers=headers)
    json = response.json()
    return jsonify(json)
@app.route("/estudiantes/<string:id>",methods=['PUT'])
def modificarEstudiante(id):
    data = request.get_json()
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/estudiantes/'+id
    response = requests.put(url, headers=headers, json=data)
    json = response.json()
    return jsonify(json)
@app.route("/estudiantes/<string:id>",methods=['DELETE'])
def eliminarEstudiante(id):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    url = dataConfig["url-backend-academic"] + '/estudiantes/' + id
    response = requests.delete(url, headers=headers)
    json = response.json()
    return jsonify(json)

##-----------------------------------------------------------------##

def limpiarURL(url):
    partes = request.path.split("/")
    return partes[1]
    ##for laParte in partes:
    ##    if re.search('\\d', laParte):
    ##        url = url.replace(laParte, "?")
    ##        return url

def validarPermiso(endPoint,metodo,idRol):
    url=dataConfig["url-backend-security"]+"/permisos-roles/validar-permiso/rol/"+str(idRol)
    tienePermiso=False
    headers = {"Content-Type": "application/json; charset=utf-8"}
    body={
     "url": endPoint,
     "metodo": metodo
    }
    response = requests.get(url, json=body, headers=headers)
    try:
        data = response.json()
        if ("_id" in data):
            tienePermiso = True
    except:
        pass
    return tienePermiso


def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data
if __name__=='__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["url-backend"]+":" + str(dataConfig["port"]))
    serve(app,host=dataConfig["url-backend"],port=dataConfig["port"])