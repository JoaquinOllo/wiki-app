from flask import Flask, session, render_template
from Server import config
import copy
from flask import request, current_app, make_response, jsonify
from Constants import ResponseCodes
from Engine import Main
import sys
from Engine import dbconnection
from flask_cors import CORS, cross_origin
from flask_session import Session

def create_app(enviroment):
    app = Flask(__name__)
    app.config.from_object(enviroment)
    return app

enviroment = config.config['development']


app = create_app(enviroment)
CORS(app,  supports_credentials=True, resources={r"*": {"origins": ["http://localhost:8080", "http://localhost:5000", "https://campaign-wiki-app.herokuapp.com"]}})
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
    """Authenticates user credentials, either by checking authorization headers, or by checking the session cookie.
    Parameters
    ----------
    name : requestData
        The request object for this call to the API
    """
    isUserValid = False

    try:
        username = requestData.authorization['username']
        password = requestData.authorization['password']
        current_app.logger.info("user calling API: {0}".format(username))

        isUserValid = dbconnection.authenticateUser(username, password)
        current_app.logger.info("authentication through headers")

    except TypeError:
        current_app.logger.info("authentication through cookies")
        sessionCookie = request.cookies.get('username', "no conectado")
        sessionUsername = session.get("username", "no conectado")
        if (sessionCookie != "no conectado" and sessionCookie == sessionUsername):
            isUserValid = True

    current_app.logger.info("valid user: {0}".format(isUserValid))

    return isUserValid

def invalidAuthResponse(responseData: object) -> object:
    """Creates and returns an invalid credentials response, by calling the make_response() Flask method, and returns it.<
    Parameters
    ----------
    name : requestData
        The request object for this call to the API
    """
    responseObj = make_response((jsonify(responseData), 401, [("Access-Control-Allow-Origin", "*")]))
    return responseObj

@app.route('/links/<field>/<value>', methods=['GET'])
def links(field, value):
    response = copy.deepcopy(responseDefault)
    if request.method == "GET":
        current_app.logger.info("call to GET links")
        if (authenticateUser(request)):
            #seek many links
            response["operationSuccess"] = ResponseCodes.SUCCESS
            for link in Main.getManyByField(value, field):
                response['links'].append(link.toJSON())
            return (response, [("Access-Control-Allow-Origin", "*")])
        else:
            return invalidAuthResponse(response)
          

@app.route('/link/<id>', methods=['GET', 'DELETE', 'PATCH'])
def link(id):
    response = copy.deepcopy(responseDefault)
    if request.method == "GET":
        if (authenticateUser(request)):
            #seek a link
            response["operationSuccess"] = ResponseCodes.SUCCESS
            link = Main.getLinkByID(id)
            response['links'].append(link.toJSON())
            return (response, [("Access-Control-Allow-Origin", "*")])
        else:
            return invalidAuthResponse(response)
    elif request.method == "DELETE":
        if (authenticateUser(request)):
            deletedLinks = Main.deleteLinkByField("_id", id)
            response['links'] = deletedLinks
            response["operationSuccess"] = ResponseCodes.SUCCESS
            return (response, [("Access-Control-Allow-Origin", "*")])
        else:
            return invalidAuthResponse(response)
    elif request.method == "PATCH":
        if (authenticateUser(request)):
            jsonData = request.get_json()
            Main.editLinkByID(id, jsonData)
            response["operationSuccess"] = ResponseCodes.SUCCESS
            link = Main.getLinkByID(id)
            response['links'].append(link.toJSON())
            return (response, [("Access-Control-Allow-Origin", "*")])
        else:
            return invalidAuthResponse(response)

@app.route('/link', methods=['PUT'])
def newLink():
    response = copy.deepcopy(responseDefault)
    if request.method == "PUT":
        if (authenticateUser(request)):
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
        else:
            return invalidAuthResponse(response)

@app.route('/login')
#@cross_origin(origins=["http://localhost:8080", "http://localhost:5000", "https://campaign-wiki-app.herokuapp.com"])
def login():
    response = copy.deepcopy(responseDefault)
    if authenticateUser(request):
        username = request.authorization['username']
        Flask.open_session(Flask, request)            
        response["operationSuccess"] = ResponseCodes.SUCCESS
        session["username"] = username
        resp = make_response(jsonify(response))
        resp.set_cookie('username', username)
    else:
        resp = make_response((jsonify(response), 401))

    return resp

@app.route('/logout')
def logout():
    session.clear()
    response = copy.deepcopy(responseDefault)
    response["operationSuccess"] = ResponseCodes.SUCCESS
    resp = make_response(jsonify(response), [("Access-Control-Allow-Origin", "*")])

    return resp

# @app.after_request # blueprint can also be app~~
# def after_request(response):
#     header = response.headers
#     header["Access-Control-Allow-Credentials"] = True
#     header['Access-Control-Allow-Origin'] = ["http://localhost:8080", "http://localhost:5000", "https://campaign-wiki-app.herokuapp.com"]
#     return response

#@app.route('/', defaults={'path': ''})
#@app.route('/<path:path>')
#def dender_vue(path):
#    return render_template("index.html")

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)