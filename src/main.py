"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Users, Objects, Resource_Centers,Days
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
    def my_users():
        if request.method == 'GET':
            users = Users.query.all()
            if not users:
                return jsonify({'msg': 'User not found'}), 404

            return jsonify( [x.serialize() for x in users] ), 200


@app.route('/hello', methods=['POST', 'GET'])
    def handle_hello():

        response_body = {
            "hello": "world"
        }

        return jsonify(response_body), 200

@app.route('/add_user', methods=['POST'])
    def add_user():
        if request.method == 'POST':
            body = request.get_json()

            db.session.add(Users(
                first_name = body["first_name"],
                last_name = body["last_name"],
                email = body["email"],
                password = body["password"],
                zip = body["zip"]
            ))
            
            db.sessions.commit()
            return jsonify({
                'msg': 'User Added!'
            })

@app.route('/add_days', methods=['POST'])
def add_day():
    if request.method == 'POST':
        body = request.get_json()

        db.session.add(Days(
            first_day = body["first_day"],
            second_day = body["second_day"],
            user_id = body["user_id"]
        ))
        
        db.session.commit()
        return jsonify({
            'msg': 'Day Added!'
        })


# @app.route('/edit_user', methods=['PUT'])
# def edit_user():
#     body = request.get_json()
#     if request.method == 'PUT':
#         first_name = body["first_name"],
#         last_name = body["last_name"],
#         email = body["email"],
#         password = body["password"],
#         zip = body["zip"]

#         db.sessions.commit()
#         return jsonify({
#             'msg': 'Info Updated!'
#         })
        

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
