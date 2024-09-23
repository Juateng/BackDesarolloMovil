
from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token ,jwt_required
from config import Config
from models import mongo

event_bp = Blueprint('event', __name__)
bcrypt = Bcrypt()

#------------------------------------------------------------------CREAR EVENTOS----------------------------------------
@event_bp.route('/create', methods=['POST'])
def register():
    #Estos son los datos que pasamos al post en formato JSON
    data = request.get_json()
    name = data.get('name')
    date = data.get('date')
    place = data.get('place')
    description = data.get('description')

    if mongo.db.events.find_one({"name": name}):
        return jsonify({"msg": "Ese evento ya existe"}), 400
    
    result = mongo.db.events.insert_one({"name":name,"date":date,"place":place,"description":description})
    if result.acknowledged:
        return jsonify({"msg": "Evento Creado Correctamente"}), 201
    else:
        return jsonify({"msg": "Hubo un error, no se pudieron guardar los datos"}),400

#------------------------------------------------------------------ELIMINAR EVENTOS----------------------------------------
@event_bp.route('/delete', methods=['DELETE'])
def erase():
    # Estos son los datos que pasamos al DELETE en formato JSON
    data = request.get_json()
    name = data.get('name')

    event = mongo.db.events.find_one({"name": name})

    if event:
        result = mongo.db.events.delete_one({"name": name})

        if result.deleted_count > 0:
            return jsonify({"msg": "Evento eliminado correctamente"}), 200
        else:
            return jsonify({"msg": "Hubo un error, no se pudo eliminar el evento"}), 400
    else:
        return jsonify({"msg": "No se encontró un evento con ese nombre"}), 404

#------------------------------------------------------------------VER EVENTOS----------------------------------------------
@event_bp.route('/info', methods=['POST'])
def datos():
    data = request.get_json()
    name = data.get('name')

    evento = mongo.db.events.find_one({"name": name})

    if evento:
        evento['_id'] = str(evento['_id'])
        return jsonify({"msg": "Evento encontrado", "Evento": evento}), 200
    else:
        return jsonify({"msg": "Evento NO encontrado"}), 404

#---------------------------------------------------------------------EDITAR EVENTOS----------------------------------------

@event_bp.route('/edit', methods=['PUT'])
def edit_event():
    data = request.get_json()
    name = data.get('name')

    event = mongo.db.events.find_one({"name": name})

    if event:
        new_date = data.get('date')
        new_place = data.get('place')
        new_description = data.get('description')

        updated_fields = {}
        if new_date:
            updated_fields['date'] = new_date
        if new_place:
            updated_fields['place'] = new_place
        if new_description:
            updated_fields['description'] = new_description

        result = mongo.db.events.update_one(
            {"name": name}, 
            {"$set": updated_fields}
        )

        if result.modified_count > 0:
            return jsonify({"msg": "Evento actualizado correctamente"}), 200
        else:
            return jsonify({"msg": "No se realizaron cambios en el evento"}), 400
    else:
        return jsonify({"msg": "No se encontró un evento con ese nombre"}), 404

