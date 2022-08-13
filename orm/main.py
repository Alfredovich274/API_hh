from flask import Flask, render_template
import time
import os
import subprocess
from orm import get_base


app = Flask(__name__)


def get_day():
    time_data = time.localtime(time.time())
    return f'{time_data.tm_mday}-{time_data.tm_mon}-{time_data.tm_year}' \
           f' {time_data.tm_hour}:{time_data.tm_min}'


@app.route("/", methods=['get'])
def index():
    return render_template('index.html')


@app.route("/contacts/")
def contacts():
    return render_template('contacts.html', name='Кириллов Павел',
                           date_time=get_day())


@app.route("/", methods=['POST'])
def index_post():
    subprocess.run("python3 parser.py", shell=True)
    book, year, author, rating = get_base()
    return render_template('result.html', book=book, year=year, author=author,
                           rating=rating)


@app.route("/result/", methods=['get'])
def result_get():
    if os.path.isfile('db_orm.sqlite'):
        book, year, author, rating = get_base()
    else:
        book, year, author, rating = False, False, False, False
    return render_template('result.html', book=book, year=year, author=author,
                           rating=rating)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
