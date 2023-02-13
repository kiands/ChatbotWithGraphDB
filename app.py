from flask import Flask, request
from flask import jsonify
import json
import tg_logic_main

app = Flask(__name__)

@app.route('/hello')
def hello():
    return jsonify(content="OK")

@app.route('/bot', methods=['POST'])
def bot():
    data = json.loads(request.get_data(as_text=True))
    res = tg_logic_main.flask_handler(data)
    return str(res)

if __name__ == "__main__": 
    app.run(port=5002)