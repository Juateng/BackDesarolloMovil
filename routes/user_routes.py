
from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token ,jwt_required
from config import Config
from models import mongo

user_bp = Blueprint('user', __name__)
bcrypt = Bcrypt()

#Definimos el endpoint para registrar un usuario
#Utilizamos el decorador @app.route('/') para definir la ruta de la URL e inmediatamente después
#la función que se ejecutará en esa ruta
@user_bp.route('/register', methods=['POST'])
def register():
    #Estos son los datos que pasamos al post en formato JSON
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if mongo.db.users.find_one({"email": email}):
        return jsonify({"msg": "Ese usuario ya existe"}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # mongo.db.users.insert_one devuelve un objeto con dos propiedades "acknowledged" 
    # si se guardo correctamente y el id del documento insertado
    result = mongo.db.users.insert_one({"username":username,"email":email,"password": hashed_password})
    if result.acknowledged:
        return jsonify({"msg": "Usuario Creado Correctamente"}), 201
    else:
        return jsonify({"msg": "Hubo un error, no se pudieron guardar los datos"}),400

#Definimos la ruta del endpoint para el login
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = mongo.db.users.find_one({'email': email})

    if user and bcrypt.check_password_hash(user['password'], password):
        access_token = create_access_token(identity=str(user["_id"]))
        return jsonify(access_token = access_token), 200
    else:
        return jsonify({"msg":"credenciales incorrectas"}), 401
    
#Creamos el endpoint protegido
@user_bp.route('/datos', methods=['POST'])
@jwt_required()
def datos():
    data = request.get_json()
    username = data.get('username')

    usuario = mongo.db.users.find_one({"username":username}, {"password":0})

    if usuario:
        usuario["_id"] = str(usuario["_id"])
        return jsonify({"msg":"Usuario encontrado", "Usuario": usuario}), 200
    else: 
        return jsonify({"msg":"Usuario NO encontrado"}), 404
