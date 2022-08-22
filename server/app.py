"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, Response, request, render_template
from tinydb import TinyDB, Query
from flask_restful import Api, Resource
from sqlalchemy.sql.expression import cast
from sqlalchemy import desc
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
import sqlalchemy as sa
import pandas as pd
import json
import bcrypt

app = Flask(__name__)
api = Api(app)
CORS(app)
auth = HTTPBasicAuth()

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    db = TinyDB('./db.json')
    user = Query()
    result = db.search(user.email == username)
    if len(result) != 0:
        email = result[0]["email"]
        hash = result[0]["password"]
        if bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8")):
            return True
        else:
            return False
    else:
        return False


class getData(Resource):
    @auth.login_required
    def get(self):
        db = request.args.get('db') 
        table = request.args.get('table') 
        server = request.args.get('server')
        engine = sa.create_engine('mssql+pyodbc://'+server+'/'+db+'?driver=SQL+Server+Native+Client+11.0')
        
        with engine.connect() as connection:
            metadata = sa.MetaData()
            census = sa.Table(table, metadata, autoload=True, autoload_with=engine)
            if table == "kri_details":
                query = sa.select([census.c.ID, census.c.kri_name, census.c.template_agg_dimension, census.c.template_agg_column, census.c.Weightage, census.c.YTD, census.c.data_type, census.c.date_field, census.c.date_from, census.c.date_to, census.c.time_frame, census.c.is_active]) 
            elif table == "kri_parameters":
                query = sa.select([census.c.ID, census.c.kri_id, census.c.param_id, census.c.Param_value])
            elif table == "RiskAlgoParameters":
                query = sa.select([census.c.ID, census.c.RiskAlgoID, census.c.Param_name, census.c.Param_type, census.c.isMandatory])
            elif table == "ValidationErrors":
                query = sa.select([census.c.ID, census.c.Year, census.c.DataType, census.c.VersionColID, census.c.RuleID, census.c.TransactionID, census.c.LZRecordID])
            elif table == "time_frames":
                query = sa.select([census.c.id, census.c.timeSpan, cast(census.c.isActive, sa.Integer)])
            elif table == "RiskyTransactions":
                query = sa.select([census.c.ID, census.c.DataType, census.c.KRIID, census.c.RiskAlgoID, census.c.TemplateAggDimension, census.c.TemplateAggDimensionValue, census.c.TemplateAggColumn, census.c.TemplateAggColumnValue, census.c.RiskScore, census.c.WeightScore, census.c.DateFrom, census.c.DateTo])
            elif table == "WarningTable":
                query = sa.select([census.c.Id, census.c.KRIID, census.c.Message, census.c.Method, census.c.ErrorColumn, census.c.ErrorTable, census.c.LineNumber, census.c.IsCritical, census.c.Timestamp])
            elif table == "lookback_configuration":
                query = sa.select([census.c.id, census.c.kriid, census.c.kriname, census.c.lookback_period])
            elif table == "RiskAlgoDictionary":
                query = sa.select([census.c.ID, census.c.AlgoName, census.c.AlgoMethod, census.c.UpdatedBy])
            elif table == "ExecutionTimeLog":
                query = sa.select([census.c.Id, census.c.Stage, census.c.Procedure, cast(census.c.TimeTaken, sa.Time), census.c.StartTime, census.c.EndTime])
            elif table == "File_Specs":
                query = sa.select([census.c.ID, census.c.FILE_TYPE, census.c.PREFIX, census.c.DATATYPE, census.c.DESC, census.c.UPDATED_DATE, census.c.UPDATED_BY, cast(census.c.ISENABLE, sa.Integer), cast(census.c.IsAppend, sa.Integer)])
            elif table == "RuleDictionary":
                query = sa.select([census.c.ID, census.c.RuleLevel, census.c.RuleCategory, census.c.RuleName, census.c.RuleCommand, census.c.RuleDescription])
            elif table == "RiskAuditLogs":
                census = sa.Table(table, metadata, sa.Column("Error Description", sa.String, key="error_description"), autoload=True, autoload_with=engine, extend_existing=True)
                query = sa.select([census.c.ID, census.c.DataType, census.c.KRIID, census.c.Status, census.c.error_description, census.c.Start_time, census.c.TimeSpan, census.c.UpdatedBy]).order_by(desc(census.c.ID))
            else:
                response = Response(status=404)
                return response
            ResultProxy = connection.execute(query)
            ResultSet = ResultProxy.fetchall()

        df = pd.DataFrame(ResultSet)
        #print(df)
        if df.empty:
            response = Response(status=200)
            return response
        df.columns = ResultSet[0].keys()
        retMap = df.to_json(orient='records')
        return retMap

    @auth.login_required
    def post(self):
        param = request.get_json()
        db = param["db"]
        server = param["server"]
        queries = param["queries"]
        engine = sa.create_engine('mssql+pyodbc://'+server+'/'+db+'?driver=SQL+Server+Native+Client+11.0')
        with engine.connect() as conn:
            for query in queries:
                try:
                    conn.execute(query)
                except:
                    response = Response(status=400)
                    return response

        response = Response(status=200)
        return response


class Databases(Resource):
    @auth.login_required
    def get(self):
        #Database connection
        server = request.args.get('server')
        engine = sa.create_engine('mssql+pyodbc://'+server+'/master?driver=SQL+Server+Native+Client+11.0') 
        query = "SELECT name FROM sys.databases WHERE name LIKE 'ComplianceMonitoring%';"
        data = pd.read_sql(query, engine)
        retMap = data['name'].to_json()
        return retMap

class JobSteps(Resource):
    @auth.login_required
    def get(self):
        server = request.args.get('server')
        job_name = request.args.get('job_name')
        engine = sa.create_engine('mssql+pyodbc://'+server+'/msdb?driver=SQL+Server+Native+Client+11.0')
        try:
            query = "EXEC sp_help_jobstep @job_name = '"+job_name+"';"
            data = pd.read_sql(query, engine)
            retMap = data['step_name'].to_json()
        except:
            response = Response(status=400)
            return response        
        return retMap

    @auth.login_required
    def post(self):
        param = request.get_json()
        job_name = param["job_name"]
        start_step = param["start_step"]
        server = param["server"]
        engine = sa.create_engine('mssql+pyodbc://'+server+'/ComplianceMonitoring?driver=SQL+Server+Native+Client+11.0')
        with engine.connect() as conn:
            query = "EXEC job_execution @job_name = '"+job_name+"', @step_name = '"+start_step+"';"
            result = pd.read_sql(query, engine)
            retMap = result['ResultValue'].to_json()

        return retMap

class User(Resource):
    #def __init__(self):
    #    db = TinyDB('./db.json')
        #self.data = dict()
    
    def post(self):
        db = TinyDB('./db.json')
        user = Query()
        param = request.get_json()
        email = param["email"]
        password = param["password"]
        new_user = param["new_user"]
        if not (email and password):
            return False
        if new_user == False:
            result = db.search(user.email == email)
            if len(result) != 0:
                email = result[0]["email"]
                hash = result[0]["password"]
                if bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8")):
                    return True
                else:
                    return False
            else:
                return False
        elif new_user == True:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            db.insert({'email': email, 'password': hashed.decode("utf-8")})
            response = Response(status=201)
            return response


api.add_resource(getData, '/getData')
api.add_resource(Databases, '/getDatabaseName')
api.add_resource(JobSteps, '/jobSteps')
api.add_resource(User, '/login')

@app.route('/')
def hello():
    """Renders a sample page."""
    return "Hello Friend!"
    #return render_template("D:/Compliance Monitoring/Logs-Screen/dist/index.html")

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)