from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models import mongo, init_db
from config import Config
from bson.json_util import ObjectId

app = Flask(__name__) #sintaxis para iniciar flask, no se cambia
app.config.from_object(Config)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

init_db(app)

#definir el endpoint para registrar un usuario
@app.route('/register', methods=['POST'])

def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if mongo.db.users.findOne({"email":email}):
        return jsonify({"msg": "Este usuario ya existe"}), 400
    
    hashed_pasword = bcrypt.generate_password_hash(password).decode('utf-8')

    result= mongo.db.users.insert_one({"username":username, "email":email, "password":hashed_pasword})
    if result.acknowledged:
        return jsonify({"msg":"usuario creado correctamente"}), 201
    else:
        return jsonify({"msg":"Hubo un error, no se pudieron guardar los datos"}), 400

if __name__ == '__main__':
    app.run(debug=True)

