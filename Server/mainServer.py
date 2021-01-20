from flask import Flask
import copy
from flask import request
from Constants import ResponseCodes
from Engine import Main
app = Flask(__name__)

#https://flask.palletsprojects.com/en/1.1.x/quickstart/
#Instructions to run flask server, on windows cmd
#cd ".\GMWiki\Server"
#set FLASK_APP=mainServer.py
#set FLASK_ENV=development
#python -m flask run

responseDefault = {
    "operationSuccess": ResponseCodes.ERROR,
    "links": [],
    "description": "Operation not executed",
    "requestMetadata": {
        "method": "",
        "params": []
    }
}

@app.route('/links/<field>/<value>', methods=['GET', 'DELETE', 'PATCH'])
def links(field, value):
    response = copy.deepcopy(responseDefault)
    if request.method == "GET":
        #seek many links
        response["operationSuccess"] = ResponseCodes.SUCCESS
        response["requestMetadata"]["method"] = request.method
        response["requestMetadata"]["params"].append ({"value": value})
        response["requestMetadata"]["params"].append ({"field": field})
        for link in Main.getManyByField(value, field):
            response['links'].append(link.toJSON())
        return response
    elif request.method == "DELETE":
        Main.deleteLinkByField(field, value)
        response["operationSuccess"] = ResponseCodes.SUCCESS
        return response
    elif request.method == "PATCH":
        jsonData = request.get_json()
        Main.editLinkPartially(value, jsonData)
        response["operationSuccess"] = ResponseCodes.SUCCESS
        return response

@app.route('/hello')
def hello():
    return 'Hello, World'