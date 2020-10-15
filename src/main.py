"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Todos
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/todos', methods=['GET'])
def all_todos():

    todos = Todos.query.all()
    all_todos = list(map(lambda x: x.serialize(), todos ))
    return jsonify(all_todos), 200


@app.route('/todos', methods=['POST'])
def create_todos():

    response = request.get_json()  

    if 'done' not in response:
        return 'Invalid', 400 
    if 'label' not in response:
        return 'Invalid', 400 

    row = Todos(done=response['done'], label=response['label'])
    db.session.add(row)
    db.session.commit()
    return jsonify(row.serialize()), 200


@app.route('/todos/<id>', methods=['DELETE'])
def delete_todos(id):
    row = Todos.query.filter_by(id=id).first_or_404()
    db.session.delete(row)
    db.session.commit()
    return jsonify(row.serialize()), 200

@app.route('/todos', methods=['PUT'])
def put_todos():
    todos = request.get_json()

    row= Todos.query.filter_by(id=todos['id']).first_or_404()

    row.done = todos['done']
    row.label = todos['label']
    db.session.commit()
    return jsonify(row.serialize()), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
