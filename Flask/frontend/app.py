from flask import Flask, render_template, request, jsonify
from datetime import datetime
from dotenv import load_dotenv
import requests

BACKEND_URL = "http://127.0.0.1:9000"

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    day_of_week = datetime.today().strftime('%A')
    current_time = datetime.now().strftime('%H:%M:%S')
    return render_template('index.html', day_of_week=day_of_week, current_time=current_time)

@app.route('/submit', methods=['POST'])
def submit():
   form_data = dict(request.form)
   response = requests.post(f"{BACKEND_URL}/submit", data=form_data)
   return response.text

@app.route('/get_data')
def get_data():
    response = requests.get(BACKEND_URL + '/view') 
    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)