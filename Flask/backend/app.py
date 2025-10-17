from flask import Flask, request, jsonify
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
    data = list(collection.find())
    for item in data:
        print(item)
        del item['_id']
    return jsonify({'data': data})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9000,debug=True)

