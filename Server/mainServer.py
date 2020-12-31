from flask import Flask
from flask import request
from Constants import ResponseCodes
from Engine import Main
app = Flask(__name__)

#Instructions to run flask server, on windows cmd
#cd ".\GMWiki\Server"
#set FLASK_APP=mainServer.py
#python -m flask run

responseDefault = {
    "operationSuccess": ResponseCodes.ERROR,
    "links": [],
    "description": "Operation not executed"
}

@app.route('/links/<field>/<value>', methods=['GET', 'DELETE', 'PATCH'])
def links(field, value):
    if request.method == "GET":
        #seek many links
        response = responseDefault
        response["operationSuccess"] = ResponseCodes.SUCCESS
        for link in Main.getManyByField(value, field):
            response['links'].append(link.toJSON())
        return response
    elif request.method == "DELETE":
        #delete 1 link
        pass
    elif request.method == "PATCH":
        #update 1 link
        pass

@app.route('/hello')
def hello():
    return 'Hello, World'