from flask import Flask, render_template
from vsearch import search4letters

app = Flask(__name__)


@app.route('/')
def hello() -> str:
    return 'FLASK, o-o, he\'s a miracle!'


@app.route('/search4')
def do_search() -> str:
    return str(search4letters('Kokolisan potasu', ))


@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search4letters')


app.run()
