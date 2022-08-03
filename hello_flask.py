from flask import Flask
from vsearch import search4letters

app = Flask(__name__)


@app.route('/')
def hello() -> str:
    return 'FLASK, o-o, he\'s a miracle!'


@app.route('/search4')
def do_search() -> str:
    return str(search4letters('Kokolisan potasu', ))


app.run()
