from flask import Flask,jsonify,request,Response,make_response, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
	app.run(debug=True)