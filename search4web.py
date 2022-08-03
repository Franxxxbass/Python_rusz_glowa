from flask import Flask, render_template, request, redirect
from vsearch import search4letters

app = Flask(__name__)


@app.route('/')
def hello() -> '302':
    return redirect('/entry')


@app.route('/search4', methods=['POST'])
def do_search() -> str:
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4letters(phrase, letters))
    title = "Here's the outcome: "
    return render_template('results.html',
                           the_results=results,
                           the_title=title,
                           the_letters=letters,
                           the_phrase=phrase,
                           )


@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search4letters')


app.run(debug=True)
