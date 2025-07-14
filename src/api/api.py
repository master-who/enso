from flask import Flask, jsonify, send_from_directory
from flask import render_template
import os
from flask import request

api = Flask(__name__)

@api.route('/')
def home():
    return render_template('index.html')

@api.route('/manifest.json')
def manifest():
    return send_from_directory('templates', 'manifest.json')

@api.route('/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js')

@api.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    save_path = os.path.join('subscription.json')
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(f"{data}\n")
    return jsonify({'status': 'success'}), 201

if __name__ == '__main__':
    api.run(debug=True)
