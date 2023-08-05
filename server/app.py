from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api
from tinydb import TinyDB, Query
import bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'this is a very strong secret key!'  # Change this!
jwt = JWTManager(app)

# Initialize the TinyDB database
db = TinyDB('D:\Compliance Monitoring\Logs-Screen\server\db.json')

# class Register for signing users 
class Register(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')

        User = Query()
        user_exists = db.search(User.username == username)

        if user_exists:
            return {"message": "User already exists"}, 400
        else:
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Store the username and hashed password in the database
            db.insert({'username': username, 'password': hashed_password.decode('utf-8')})
            return {"message": "User created successfully"}, 201    

# class Login for logging in users
class Login(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')

        User = Query()
        user = db.search(User.username == username)
        
        # Check the password against the hashed password in the database
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user[0]['password'].encode('utf-8')):
                access_token = create_access_token(identity=username)
                return {"message": "Login succeeded!", "access_token": access_token}, 200
            else:
                return {"message": "Invalid credentials"}, 401
        else:
            return {"message": "User does not exist"}, 400

class Protected(Resource):
    @jwt_required()
    def get(self):
        return {"message": "You are authorized!"}, 200

api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(Protected, '/protected')

if __name__ == '__main__':
    app.run(debug=True)
