from flask import Flask, request, render_template
from datetime import datetime
from dotenv import load_dotenv
import os 
from pymongo.mongo_client import MongoClient

load_dotenv()

# MongoDB connection setup 
uri = os.getenv("MONGODB_URI")
client = MongoClient(uri)
db = client.test
collection = db['flask-tutorial']

app = Flask(__name__)

@app.route('/')
def home():
    day_of_week = datetime.today().strftime('%A')
    current_time = datetime.now().strftime('%H:%M:%S')
    return render_template('index.html', day_of_week=day_of_week, current_time=current_time)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    
    if name and email:
        # Insert data into MongoDB
        collection.insert_one({'name': name, 'email': email})
        return f"Thank you {name}, your email {email} has been recorded!"
    else:
        return "Please provide both name and email."

@app.route('/view')
def view():
    entries = list(collection.find({}, {'_id': 0}))
    return render_template('view.html', entries=entries)


if __name__ == '__main__':
    app.run(debug=True)

# python -m pip install "pymongo[srv]==3.11"