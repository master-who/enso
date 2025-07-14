from flask import Flask, jsonify

api = Flask(__name__)

@api.route('/')
def home():
    return jsonify({"message": "Welcome to the Enso API!"})

if __name__ == '__main__':
    api.run(debug=True)