### Backend usando Pyhton Flask y MongoDB con JWT y Bcrypt ###
### Universidad Anahuac Mayab
### 31-08-2024, Fabricio Suárez
### Prog de Dispositivos Móviles


#importamos todo lo necesario para que funcione el backend
from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models import mongo, init_db
from config import Config
from bson.json_util import ObjectId
from flask_bcrypt import Bcrypt
from routes.user_routes import user_bp
from routes.events_routes import event_bp
from routes.ticket_routes import ticket_bp

#Inicializamos la aplicación y usamos el config file
app = Flask(__name__)
app.config.from_object(Config)

#Inicializamos a bcrypt y jwt
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

#Inicializamos el acceso a MongoDB
init_db(app)

app.register_blueprint(user_bp)
app.register_blueprint(event_bp)
app.register_blueprint(ticket_bp)

# En Python, cada archivo tiene una variable especial llamada __name__.
# Si el archivo se está ejecutando directamente (no importado como un módulo en otro archivo), 
# __name__ se establece en '__main__'.
# Esta condición verifica si el archivo actual es el archivo principal que se está ejecutando. 
# Si es así, ejecuta el bloque de código dentro de la condición.
# app.run() inicia el servidor web de Flask.
# El argumento debug=True  inicia el servidor web de desarrollo de Flask con el modo de 
# depuración activado, # lo que permite ver errores detallados y reiniciar automáticamente
# el servidor cuando se realizan cambios en el código. (SERIA COMO EL NODEMON)
if __name__ == '__main__':
    app.run(debug=True)