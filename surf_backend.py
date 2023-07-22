from flask import Flask, request, jsonify
from flask_cors import CORS
import wolframalpha

app = Flask(__name__)
CORS(app)

# Replace 'YOUR_WOLFRAM_ALPHA_APP_KEY' with your actual WolframAlpha app key
wolfram_alpha_app_key = 'JGUTQ4-RG973Q6L5E'
client = wolframalpha.Client(wolfram_alpha_app_key)

@app.route('/query', methods=['POST', 'GET'])
def process_query():
    try:
        data = request.get_json()
        query = data.get('query', '')
        

        # Process the user query using WolframAlpha API
        res = client.query(query)
        output = next(res.results).text

        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='192.160.161.157')



