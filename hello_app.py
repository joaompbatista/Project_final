from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route('/sample', methods=['POST'])
def running():
    message = request.get_json(force = True)
    name = message['name']
    response = {
        'greetings':'Hello, ' + name +'!'
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)