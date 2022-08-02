from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello() -> str:
    return 'FLASK, o-o, he\'s a miracle!'


app.run()
