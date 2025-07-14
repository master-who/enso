from flask import Flask, jsonify, send_from_directory
from flask import render_template
import os

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

if __name__ == '__main__':
    api.run(debug=True)
