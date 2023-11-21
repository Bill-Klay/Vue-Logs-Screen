from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from tinydb import TinyDB, Query
import bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.sql import text
from sqlalchemy.exc import OperationalError
import pandas as pd
import logging

app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'this is a very strong secret key!'  # Change this!
jwt = JWTManager(app)

# Configure server logs
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)  # Set the minimum log level to INFO

# Initialize the TinyDB database
# Global variables can be read anywhere without specifying, but need to declared within the function when writing to it
db = TinyDB('.\db.json')
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
                app.logger.warning('Invalid login attempt')
                return {"message": "Invalid credentials", "color": "error"}, 200
        else:
            app.logger.warning('Invalid login attempt')
            return {"message": "User does not exist", "color": "error"}, 200

class Database(Resource):
    @jwt_required()
    def put(self):
        global database, engine
        parser = reqparse.RequestParser()
        parser.add_argument('db', type=str, required=True, help='Database name is required') # also has a default parameter
        args = parser.parse_args()
        database = args['db']
        engine = create_engine('mssql+pyodbc://'+server+'/'+database+'?driver=SQL+Server+Native+Client+11.0')
        try:
            connection = engine.connect()
            connection.close()
            return {'message': 'Database connection successful', 'color': 'success'}, 200
        except OperationalError as e:
            app.logger.error('Error occurred: %s', e)
            return {'message': 'Database connection failed: ' + str(e), 'color': 'error'}, 500
    
    @jwt_required()
    def get(self):
        # Fetch table names matching 'validation'
        global engine
        query = text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE '%Validation'")
        try:
            with engine.connect() as connection:
                result = connection.execute(query)
                table_names = [row[0] for row in result]

                # Get count of rows in each table and store results in a dictionary
                data_counts = {}
                for table in table_names:
                    query = text(f'SELECT COUNT(*) AS [count] FROM {table}')
                    result = connection.execute(query)
                    count = [row[0] for row in result][0]
                    data_counts[table] = count

            return jsonify(data_counts)
        except OperationalError as e:
            app.logger.error('Error occurred: %s', e)
            return {'message': 'Query execution failed: ' + str(e), 'color': 'error'}, 500



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
    
    @jwt_required()
    def put(self):
        global engine
        parser = reqparse.RequestParser()
        parser.add_argument('queries', action='append', required=True, help='SQL queries are required')
        args = parser.parse_args()
        queries = args["queries"]
        with engine.connect() as conn:
            for query in queries:
                try:
                    conn.execute(query)
                except OperationalError as e:
                    app.logger.error('Error occurred: %s', e)
                    return {"message": "Could not reset: " + str(e) , "color": "error"}, 400

        return {"message": "Data refreshed. Execute Job to see effects.", "color": "success"}, 200

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
        except OperationalError as e:
            app.logger.error('Error occurred: %s', e)
            return Response(status=400)
        
class JobSteps(Resource):
    @jwt_required()
    def get(self):
        global server
        engine = create_engine('mssql+pyodbc://'+server+'/msdb?driver=SQL+Server+Native+Client+11.0')
        job_name = request.args.get('job_name')
        try:
            query = "EXEC sp_help_jobstep @job_name = '"+job_name+"';"
            data = pd.read_sql(query, engine)
            retMap = data['step_name'].to_json()
        except OperationalError as e:
            app.logger.error('Error occurred: %s', e)
            return Response(status=400)      
        return retMap

    @jwt_required()
    def put(self):
        global engine
        param = request.get_json()
        job_name = param["job_name"]
        start_step = param["start_step"]
        query = "EXEC job_execution @job_name = '"+job_name+"', @step_name = '"+start_step+"';"
        result = pd.read_sql(query, engine)
        retMap = result['ResultValue'].to_json()

        return retMap
    
    @jwt_required()
    def post(self):
        global engine
        try:
            query = "SELECT name FROM msdb.dbo.sysjobs WHERE name LIKE '%ComplianceMonitoring%';"
            result = pd.read_sql(query, engine)
            retMap = result['name'].to_json()
            return retMap
        except OperationalError as e:
            app.logger.error('Error occurred: %s', e)
            return None, 200

api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(Data, '/getdata')
api.add_resource(Server, '/server')
api.add_resource(Database, '/database')
api.add_resource(JobSteps, '/jobsteps')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
