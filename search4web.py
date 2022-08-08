from flask import Flask, render_template, request, escape
from vsearch import search4letters

app = Flask(__name__)


def log_request(req: 'flask_request', res: str) -> None:
    """Logs details and results of web request"""
    with open('vsearch.log', 'a') as log:
        print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')


@app.route('/search4', methods=['POST'])
def do_search() -> str:
    """Extracts given data; conducts search, returns results """
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4letters(phrase, letters))
    title = "Here's the outcome: "
    log_request(request, results)
    return render_template('results.html',
                           the_results=results,
                           the_title=title,
                           the_letters=letters,
                           the_phrase=phrase,
                           )


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    """Displays HTML template for application"""
    return render_template('entry.html', the_title='Welcome to search4letters')


@app.route('/viewlog')
def view_the_log() -> 'html':
    """Displays contents of request log file"""
    with open('vsearch.log') as log:
        contents = []
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Form data', 'Client\'s adress', 'Users agent', 'Results')
    return render_template('viewlog.html',
                           the_title='Logs view',
                           the_row_titles=titles,
                           the_data=contents,)


if __name__ == '__main__':
    app.run(debug=True)
