from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token ,jwt_required
from config import Config
from models import mongo

ticket_bp = Blueprint('ticket', __name__)
bcrypt = Bcrypt()

#------------------------------------------------------------------CREAR TICKETS----------------------------------------
@ticket_bp.route('/ticket-in', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    name = data.get('name')

    if mongo.db.tickets.find_one({"name": name, "email": email}):
        return jsonify({"msg": "El usuario ya ha registrado un boleto para este evento"}), 400

    event = mongo.db.events.find_one({"name": name}) 
    if event:
        event_date = event.get('date')
        event_place = event.get('place')
        event_description = event.get('description')
    else:
        return jsonify({"msg": "No se encontró información del evento"}), 404

    # Registrar el boleto con la información del evento
    result = mongo.db.tickets.insert_one({
        "username": username,
        "email": email,
        "name": name,
        "event_date": event_date,
        "event_place": event_place,
        "event_description": event_description
    })

    if result.acknowledged:
        return jsonify({"msg": "Ticket creado correctamente"}), 201
    else:
        return jsonify({"msg": "Hubo un error, no se pudieron guardar los datos"}), 400
    
#------------------------------------------------------------------Ver TICKETS----------------------------------------
@ticket_bp.route('/ticket-info', methods=['POST'])
def view_ticket():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')

    # Buscar el ticket por el nombre del usuario y el nombre del evento
    ticket = mongo.db.tickets.find_one({"email": email, "name": name})

    if ticket:
        # Convertir el ObjectId a string para que sea serializable
        ticket['_id'] = str(ticket['_id'])

        # Retornar los detalles del ticket
        return jsonify({
            "msg": "Ticket encontrado",
            "ticket": ticket
        }), 200
    else:
        return jsonify({"msg": "No se encontró un ticket para este usuario y evento"}), 404

