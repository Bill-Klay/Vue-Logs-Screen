from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from tinydb import TinyDB, Query
import bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.sql.expression import cast
import pandas as pd

app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'this is a very strong secret key!'  # Change this!
jwt = JWTManager(app)

# Initialize the TinyDB database
# Global variables can be read anywhere without specifying, but need to declared within the function when writing to it
db = TinyDB('D:\Compliance Monitoring\Logs-Screen\server\db.json')
server, database, engine = None, None, None

# class Register for signing users 
class Register(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')

        User = Query()
        user_exists = db.search(User.username == username)

        if user_exists:
            return {"message": "User already exists", "color": "error"}, 200
        else:
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Store the username and hashed password in the database
            db.insert({'username': username, 'password': hashed_password.decode('utf-8')})
            return {"message": "User created successfully", "color": "success"}, 201    

# class Login for logging in users
class Login(Resource):
    def post(self):
        username = request.json.get('username') # username and password are already in JSON format hence the return statement does not require to jsonified
        password = request.json.get('password')

        User = Query()
        user = db.search(User.username == username)
        
        # Check the password against the hashed password in the database
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user[0]['password'].encode('utf-8')):
                access_token = create_access_token(identity=username)
                return {"message": "Login successful!", "color": "success", "access_token": access_token}, 202
            else:
                return {"message": "Invalid credentials", "color": "error"}, 200
        else:
            return {"message": "User does not exist", "color": "error"}, 200

class Database(Resource):
    @jwt_required()
    def get(self):
        # global server, engine, database
        # database = request.args.get('db')  # whilst here the parameters are not in JSON hence need to be jsonified before being returned
        global database
        parser = reqparse.RequestParser()
        parser.add_argument('db', type=str, required=True, help='Database name is required', location='url') # also has a default parameter
        args = parser.parse_args()
        database = args['db']
        engine = create_engine('mssql+pyodbc://'+server+'/'+database+'?driver=SQL+Server+Native+Client+11.0')
        try:
            connection = engine.connect()
            connection.close()
            return {'message': 'Database connection successful', 'color': 'success'}, 200
        except Exception as e:
            return {'message': 'Database connection failed: ' + str(e), 'color': 'error'}, 500

class Data(Resource):
    @jwt_required()
    def get(self):
        # db = request.args.get('db') 
        table_name = request.args.get('table') 
        # server = request.args.get('server')
        # engine = create_engine('mssql+pyodbc://'+server+'/'+db+'?driver=SQL+Server+Native+Client+11.0')

        TABLES_COLUMNS_MAP = {
            'kri_details': ['ID', 'kri_name', 'template_agg_dimension', 'template_agg_column', 'Weightage', 'YTD', 'data_type', 'date_field', 'date_from', 'date_to', 'time_frame', 'is_active'],
            'kri_parameters': ['ID', 'kri_id', 'param_id', 'Param_value'],
            'RiskAlgoParameters': ['ID', 'RiskAlgoID', 'Param_name', 'Param_type', 'isMandatory'],
            'ValidationErrors': ['ID', 'Year', 'DataType', 'VersionColID', 'RuleID', 'TransactionID', 'LZRecordID'],
            'time_frames': ['id', 'timeSpan', 'isActive'],
            'RiskyTrnsactions': ['ID', 'DataType', 'KRIID', 'RiskAlgoID', 'TemplateAggDimension', 'TemplateAggDimensionValue', 'TemplateAggColumn', 'TemplateAggColumnValue', 'RiskScore', 'WeightScore', 'DateFrom', 'DateTo'],
            'WarningTable': ['Id', 'KRIID', 'Message', 'Method', 'ErrorColumn', 'ErrorTable', 'LineNumber', 'IsCritical', 'Timestamp'],
            'lookback_configuration': ['id', 'kriid', 'kriname', 'lookback_period'],
            'File_Specs': ['ID', 'FILE_TYPE', 'PREFIX', 'DATATYPE', 'DESC', 'UPDATED_DATE', 'UPDATED_BY', 'ISENABLE', 'IsAppend']
        }
        
        with engine.connect() as connection:
            metadata = MetaData()
            table_to_query = Table(table_name, metadata, autoload_with=engine)

            columns_to_select = [getattr(table_to_query.c, col) for col in TABLES_COLUMNS_MAP[table_name]]
            query = select(*columns_to_select)
            ResultProxy = connection.execute(query)
            ResultSet = ResultProxy.fetchall()
            columns = ResultProxy.keys()

        df = pd.DataFrame(ResultSet, columns=columns)

        if df.empty:
            return {"message": "No data for " + table_name, "color": "warning"}, 200

        return df.to_json(orient='records')

class Server(Resource):
    @jwt_required()
    def get(self):
        # Server connection
        global server
        try:
            server = request.args.get('server')
            engine = create_engine('mssql+pyodbc://'+server+'/master?driver=SQL+Server+Native+Client+11.0') 
            query = "SELECT name FROM sys.databases WHERE name LIKE 'ComplianceMonitoring%';"
            data = pd.read_sql(query, engine)
            retMap = data['name'].to_json()
            return retMap
        except Exception as Arg:
            f = open("./server_logs.txt", "a")
            # writing in the file
            f.write(str(Arg))
            f.close()
            return Response(status=400)

api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(Data, '/getdata')
api.add_resource(Server, '/server')
api.add_resource(Database, '/database')

if __name__ == '__main__':
    app.run(debug=True)
