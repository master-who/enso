from flask import Flask, jsonify, send_from_directory
from flask import render_template
import os
import sys
from pathlib import Path
from flask import request

# Add lib directory to path for notify import
sys.path.append(str(Path(__file__).parent.parent / "lib"))
import notify

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

@api.route('/subscriptions/<thread>/', methods=['POST'])
def subscribe(thread):
    data = request.get_json()

    # Try to add subscription
    success, message = notify.subscribe(thread, data)
    if not success:
        print('Error:', message)
        if message.endswith("is not supported"):
            return jsonify({'error': message}), 404
        return jsonify({'error': message}), 400

    return jsonify({'status': 'success', 'message': message}), 201

if __name__ == '__main__':
   api.run(debug=True)
