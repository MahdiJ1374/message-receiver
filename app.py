from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
from datetime import datetime
import os
from flask import render_template

app = Flask(__name__)
CORS(app)

DATA_FILE = 'messages.csv'

# اگر فایل وجود نداره، هدر اضافه کن
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp','text'])

@app.route('/submit', methods=['POST'])
def submit():
    payload = request.get_json(force=True)
    text = payload.get('text', '').strip()

    if not text:
        return jsonify({"status":"error","message":"no text provided"}), 400

    with open(DATA_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.utcnow().isoformat(), text])

    return jsonify({"status":"ok"})

@app.route("/")
def home():
    return render_template("index.html")

