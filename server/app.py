"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from sqlalchemy.sql.expression import cast
from flask_cors import CORS
import sqlalchemy as sa
import pandas as pd
import json

app = Flask(__name__)
api = Api(app)
CORS(app)

class getData(Resource):
    def get(self):
        db = request.args.get('db') 
        table = request.args.get('table') 
        server = request.args.get('server')
        engine = sa.create_engine('mssql+pyodbc://'+server+'/'+db+'?driver=SQL+Server+Native+Client+11.0', echo=True)
        
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
            else:
                return 404
            ResultProxy = connection.execute(query)
            ResultSet = ResultProxy.fetchall()

        df = pd.DataFrame(ResultSet)
        if df.empty:
            return 200
        df.columns = ResultSet[0].keys()
        retMap = df.to_json(orient='records')
        return retMap

    def post(self):
        param = request.get_json()
        db = param["db"]
        server = param["server"]
        queries = param["queries"]
        engine = sa.create_engine('mssql+pyodbc://'+server+'/'+db+'?driver=SQL+Server+Native+Client+11.0', echo=True)
        with engine.connect() as conn:
            for query in queries:
                try:
                    conn.execute(query)
                except:
                    return 400

        return 200


class Databases(Resource):
    def get(self):
        #Database connection
        server = request.args.get('server')
        engine = sa.create_engine('mssql+pyodbc://'+server+'/master?driver=SQL+Server+Native+Client+11.0', echo=True)
        query = "SELECT name FROM sys.databases WHERE name LIKE 'ComplianceMonitoring%';"
        data = pd.read_sql(query, engine)
        retMap = data['name'].to_json()
        return retMap

class JobSteps(Resource):
    def get(self):
        server = request.args.get('server')
        job_name = request.args.get('job_name')
        engine = sa.create_engine('mssql+pyodbc://'+server+'/msdb?driver=SQL+Server+Native+Client+11.0', echo=True)
        try:
            query = "EXEC sp_help_jobstep @job_name = '"+job_name+"';"
            data = pd.read_sql(query, engine)
            retMap = data['step_name'].to_json()
        except:
            return 400        
        return retMap

    def post(self):
        param = request.get_json()
        job_name = param["job_name"]
        start_step = param["start_step"]
        server = param["server"]
        engine = sa.create_engine('mssql+pyodbc://'+server+'/ComplianceMonitoring?driver=SQL+Server+Native+Client+11.0', echo=True)
        with engine.connect() as conn:
            query = "EXEC job_execution @job_name = '"+job_name+"', @step_name = '"+start_step+"';"
            result = pd.read_sql(query, engine)
            retMap = result['ResultValue'].to_json()

        return retMap

api.add_resource(getData, '/getData')
api.add_resource(Databases, '/getDatabaseName')
api.add_resource(JobSteps, '/jobSteps')

@app.route('/')
def hello():
    """Renders a sample page."""
    return "Hello World!"

#if __name__ == '__main__':
    #import os
    #HOST = os.environ.get('SERVER_HOST', 'localhost')
    #try:
    #    PORT = int(os.environ.get('SERVER_PORT', '5555'))
    #except ValueError:
    #    PORT = 5555
    #app.run(HOST, PORT)