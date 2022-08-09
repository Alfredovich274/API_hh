from flask import Flask, render_template
import time
import json
import os
import subprocess


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
    if os.path.isfile('100books.json'):
        with open('100books.json', 'r') as info:
            data = json.load(info)
    return render_template('result.html', data=data)


@app.route("/result/", methods=['get'])
def result_get():
    data = False
    if os.path.isfile('100books.json'):
        with open('100books.json', 'r') as info:
            data = json.load(info)
            print(data)
    return render_template('result.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
