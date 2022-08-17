import mysql
from flask import Flask, render_template, request, escape
from vsearch import search4letters
from mysql import connector

app = Flask(__name__)


def get_browser(req: 'flask_request') -> str:
    """splits request.user_agent to get name of browser"""
    lst = str(req.user_agent).split()
    browser = lst[-1].split('/')
    return browser[0]


def log_request(req: 'flask_request', res: str) -> None:
    """Logs details and results of web request and stores data in database"""
    dbconfig = { 'host': '127.0.0.1',
                 'user': 'search',
                 'password': 'searchpasswd',
                 'database': 'vsearchlogDB',}

    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """insert into log (phrase, letters, ip, browser_string, results)
    values (%s, %s, %s, %s, %s)"""
    cursor.execute(_SQL, (req.form['phrase'],
                          req.form['letters'],
                          req.remote_addr,
                          get_browser(req),
                          res,)
                   )
    conn.commit()
    cursor.close()


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
