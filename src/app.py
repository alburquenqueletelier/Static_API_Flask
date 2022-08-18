"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET', 'DELETE'])
def member_action(id):

    member = jackson_family.get_member(id)
    if member:
        if request.method == 'GET':
            # del member[0]["last_name"]
            return jsonify(member[0]), 200
        elif request.method == 'DELETE':
            jackson_family.delete_member(id)
            return jsonify({
                "done": True
            })
        else:
            return jsonify({
                "Error": "Metodo no permitido"
            }), 400
    else:
        return jsonify({
            "message": f"No existe user con el id={id}"
        }), 404

@app.route('/member', methods=['POST'])
def add_new_member():

    member = request.get_json()
    if len(member["first_name"])>0 and member["age"]>=0 and len(member["lucky_numbers"]) > 0:
        jackson_family.add_member({
            "id": member["id"] if "id" in member else None,
            "first_name": member["first_name"],
            "age": member["age"],
            "lucky_numbers": member["lucky_numbers"]
        })
        return jsonify({
            "message": "Nuevo miembro creado exitosamente"
        }), 200
    else:
        return jsonify({
            "message": "No se pudo crear el usuario"
        }), 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
