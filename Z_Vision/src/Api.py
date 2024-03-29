from flask import Flask, jsonify, request, make_response

#Librerías para crea la base de datos
from db_conn import create_db_table

#Funciones con inyecciones SQL de los datos
import app_controller

#Librerías para consumir datos desde un cliente
from flask_cors import CORS

#Librerías enlazadas al API VISION
from Detection import run_detection, run_detection_on_image
import cv2
import numpy as np
import base64

#Libreria para tomar la fecha del sistema
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Endpoint HTTP saludo API de usuario
@app.route("/", methods=["GET"])
def api_Welcome_user():
    return("Has iniciado el API de gestión de usuarios")

# Endpoint HTTP creación de usuario
@app.route("/api/v1/users/create", methods=["POST"])
def api_create_user():
    user_details = request.get_json()
    age = user_details["age"]
    gender = user_details["gender"]
    emotion = user_details["emotion"]
    DateCreated = user_details["DateCreated"]
    result = app_controller.create_user(age, gender, emotion, DateCreated)
    return jsonify(result)

# Endpoint HTTP listado de usuarios
@app.route('/api/v1/users', methods=["GET"])
def api_get_users():
    result = app_controller.get_users()
    return jsonify(result)

# Endpoint HTTP listado de usuario por id
@app.route("/api/v1/users/{id}", methods=["GET"])
def api_get_user_by_id(id):
    result = app_controller.get_user_by_id(id)
    return jsonify(result)

# Endpoint HTTP actualización de usuario
@app.route("/api/v1/users/update/{id}", methods=["PUT"])
def api_update_user(id):
    user_details = request.get_json()
    #id = user_details["id"]
    age = user_details["age"]
    gender = user_details["gender"]
    emotion = user_details["emotion"]
    DateCreated = user_details["DateCreated"]
    result = app_controller.update_user(id, age, gender, emotion, DateCreated)
    return jsonify(result)

# Endpoint HTTP eliminación de usuario
@app.route("/api/v1/users/delete/<id>", methods=["DELETE"])
def api_delete_user(id):
    result = app_controller.delete_user(id)
    return make_response(jsonify(result), 200)

# Endpoint HTTP para detección y ingreso de un nuevo usuario
@app.route('/api/v1/detect', methods=['POST'])
def api_detect():
    # Obtén la imagen de la solicitud
    image_data = request.json['image']
    image_data = image_data.split(',')[1]
    # Decodifica la imagen
    image_data = base64.b64decode(image_data)
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Ejecuta la detección en la imagen
    results = run_detection(image)
    if results:
        first_result = results[0]
        age = first_result["age"]
        gender = first_result["gender"]
        emotion = first_result["emotion"]

    else:
        age = None
        gender = None
    #emotion = results["emotion"]
    DateCreated = datetime.now().strftime("%d-%m-%Y")
    result = app_controller.create_user(age, gender,emotion, DateCreated)

    # Devuelve los resultados
    return {'results': result}

# Endpoint HTTP para detección en tiempo real
@app.route('/api/v1/detect_streaming', methods=['POST'])
def api_detect_streaming():
    data = request.get_json()
    base64_image = data['image']
    
    # Decodificar la imagen base64.
    image_data = base64.b64decode(base64_image)
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Ejecutar la detección en la imagen.
    boxes = run_detection_on_image(image)
    if boxes:
        return jsonify(boxes)
    else:
        return jsonify({'error': 'No detection results'})
    
# Endpoint HTTP datos para las metricas de la app
@app.route("/api/v1/metrics", methods=["GET"])
def api_get_metrics():
    ages  = app_controller.get_ages()
    emotions = app_controller.get_emotions()
    result = ages, emotions
    return jsonify(result)


"""
Enable CORS. Disable it if you don't need CORS
"""

@app.before_request
def before_request():
    if request.method == 'OPTIONS':  # Respond to preflight requests
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
        response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
        return response

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*" # <- You can change "*" for a domain for example "http://localhost"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response


if __name__ == "__main__":
    create_db_table()
    app.run(host='0.0.0.0', port=8000, debug=False)