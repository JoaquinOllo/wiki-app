from flask import Flask, session
from Server import config
import copy
from flask import request, current_app, make_response, jsonify
from Constants import ResponseCodes
from Engine import Main
import sys
from Engine import dbconnection
from flask_cors import CORS
from flask_session import Session

def create_app(enviroment):
    app = Flask(__name__)
    app.config.from_object(enviroment)
    return app

enviroment = config.config['development']


app = create_app(enviroment)
CORS(app)
Session(app)


#https://flask.palletsprojects.com/en/1.1.x/quickstart/
#Instructions to run flask server, on windows cmd
#cd ".\GMWiki\"
#set FLASK_APP=main.py
#set FLASK_ENV=development
#python -m flask run

responseDefault = {
    "operationSuccess": ResponseCodes.ERROR,
    "links": []
}

def authenticateUser(requestData: object) -> bool:
    isUserValid = False

    try:
        username = requestData.authorization['username']
        password = requestData.authorization['password']
        current_app.logger.info("user calling API: {0}".format(username))

        isUserValid = dbconnection.authenticateUser(username, password)

    except TypeError:
        sessionCookie = request.cookies.get('username', "no conectado")
        sessionUsername = session.get("username", "no conectado")
        if (sessionCookie != "no conectado" and sessionCookie == sessionUsername):
            isUserValid = True

    current_app.logger.info("valid user: {0}".format(isUserValid))

    return isUserValid

@app.route('/links/<field>/<value>', methods=['GET'])
def links(field, value):
    response = copy.deepcopy(responseDefault)
    if request.method == "GET":
        current_app.logger.info("call to GET links")
        try:
            if (authenticateUser(request)):
                #seek many links
                response["operationSuccess"] = ResponseCodes.SUCCESS
                for link in Main.getManyByField(value, field):
                    response['links'].append(link.toJSON())
                return (response, [("Access-Control-Allow-Origin", "*")])
            else:
                responseObj = make_response((jsonify(response), 401, [("Access-Control-Allow-Origin", "*")]))
                return responseObj
        except TypeError:
            responseObj = make_response((jsonify(response), 401, [("Access-Control-Allow-Origin", "*")]))
            return responseObj
        except:
            responseObj = make_response((jsonify(response), 500, [("Access-Control-Allow-Origin", "*")]))
            return responseObj            

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
        return (response, [("Access-Control-Allow-Origin", "*")])
    elif request.method == "PATCH":
        jsonData = request.get_json()
        Main.editLinkByID(id, jsonData)
        response["operationSuccess"] = ResponseCodes.SUCCESS
        link = Main.getLinkByID(id)
        response['links'].append(link.toJSON())
        return (response, [("Access-Control-Allow-Origin", "*")])

@app.route('/link', methods=['PUT'])
def newLink():
    response = copy.deepcopy(responseDefault)
    if request.method == "PUT":
        jsonData = request.get_json()
        try:
            createdLinks = Main.registerSimpleLink(jsonData)
            response["operationSuccess"] = ResponseCodes.SUCCESS
            response["links"] = createdLinks
        except TypeError:
            response["description"] = ResponseCodes.FORMATINPUTERROR
        except:
            response["description"] = ResponseCodes.UNKNOWNERROR
        return (response, [("Access-Control-Allow-Origin", "*")])

@app.route('/login')
def login():
    response = copy.deepcopy(responseDefault)
    if authenticateUser(request):
        username = request.authorization['username']
        Flask.open_session(Flask, request)            
        response["operationSuccess"] = ResponseCodes.SUCCESS
        session["username"] = username
        resp = make_response(jsonify(response), [("Access-Control-Allow-Origin", "*")])
        resp.set_cookie('username', username)
    else:
        resp = make_response((jsonify(response), 401, [("Access-Control-Allow-Origin", "*")]))

    return resp


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)