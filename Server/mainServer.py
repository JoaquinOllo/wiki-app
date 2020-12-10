from flask import Flask
from Engine import Main
app = Flask(__name__)

@app.route('/')
def index():
    return  Main.getLink("articulo").getFullText()

@app.route('/hello')
def hello():
    return 'Hello, World'