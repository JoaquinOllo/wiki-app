from flask import Flask
from Server import config
import copy
from flask import request, current_app
from Constants import ResponseCodes
from Engine import Main
import sys

def create_app(enviroment):
    app = Flask(__name__)
    app.config.from_object(enviroment)
    return app

enviroment = config.config['development']


app = create_app(enviroment)


#https://flask.palletsprojects.com/en/1.1.x/quickstart/
#Instructions to run flask server, on windows cmd
#cd ".\GMWiki\Server"
#set FLASK_APP=mainServer.py
#set FLASK_ENV=development
#python -m flask run

responseDefault = {
    "operationSuccess": ResponseCodes.ERROR,
    "links": [],
#    "requestMetadata": {
#        "method": "",
#        "params": []
#    }
}

@app.route('/links/<field>/<value>', methods=['GET'])
def links(field, value):
    response = copy.deepcopy(responseDefault)
    if request.method == "GET":
        current_app.logger.info("call to GET links")
        #seek many links
        response["operationSuccess"] = ResponseCodes.SUCCESS
        for link in Main.getManyByField(value, field):
            response['links'].append(link.toJSON())
        return (response, [("Access-Control-Allow-Origin", "*")])

@app.route('/link/<id>', methods=['GET', 'DELETE', 'PATCH'])
def link(id):
    response = copy.deepcopy(responseDefault)
    if request.method == "GET":
        #seek a link
        response["operationSuccess"] = ResponseCodes.SUCCESS
        link = Main.getLinkByID(id)
        response['links'].append(link.toJSON())
        return (response, [("Access-Control-Allow-Origin", "*")])
    elif request.method == "DELETE":
        deletedLinks = Main.deleteLinkByField("_id", id)
        response['links'] = deletedLinks
        response["operationSuccess"] = ResponseCodes.SUCCESS
        return response
    elif request.method == "PATCH":
        jsonData = request.get_json()
        Main.editLinkByID(id, jsonData)
        response["operationSuccess"] = ResponseCodes.SUCCESS
        link = Main.getLinkByID(id)
        response['links'].append(link.toJSON())
        return response

@app.route('/hello')
def hello():
    current_app.logger.info("call to hello")
    return 'Hello, World'

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)