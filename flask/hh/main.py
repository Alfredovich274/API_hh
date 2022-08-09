from flask import Flask, render_template, request
import time
import json
import os
import subprocess


app = Flask(__name__)
# Глобальные переменные
busy = False


def get_day():
    time_data = time.localtime(time.time())
    return f'{time_data.tm_mday}-{time_data.tm_mon}-{time_data.tm_year}' \
           f' {time_data.tm_hour}:{time_data.tm_min}'


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/contacts/")
def contacts():
    return render_template('contacts.html', name='Кириллов Павел',
                           date_time=get_day())


@app.route("/form/", methods=['GET'])
def form_get():
    return render_template('form.html')


@app.route("/form/", methods=['POST'])
def form_post():
    keywords = request.form['keywords']
    keywords = keywords if keywords else None
    region = request.form['region']
    region = region if region else None
    employment = request.form['type_of_employment']
    employment = employment if employment != 'Выберите...' else None
    schedule = request.form['schedule']
    schedule = schedule if schedule != 'Выберите...' else None
    if keywords or region or employment or schedule:
        # global busy
        # busy = True
        params = {
            'text': keywords,
            'area': region,
            'employment': employment,
            'schedule': schedule
        }
        with open('params.json', 'w') as log:
            json.dump(params, log)

        subprocess.run("python3 analysis_hh.py", shell=True)

        if os.path.isfile('info.json'):
            with open('info.json', 'r') as info:
                data = json.load(info)
    return render_template('total.html', data=data)


@app.route("/result/")
def result():
    data = False
    if os.path.isfile('database.json'):
        with open('database.json', 'r') as database:
            data = json.load(database)
    return render_template('result.html', data=data)


@app.route("/total/")
def total():
    data = False
    if os.path.isfile('info.json'):
        with open('info.json', 'r') as info:
            data = json.load(info)
    return render_template('total.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
