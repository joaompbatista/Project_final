from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def my_function():
    return "Another try"

@app.route('/hello', methods=['post','get'])
def hello():   
    if request.method == 'POST':
        message = request.get_json(force = True)
        name = message['name']
        response = {'greeting':'Hello, ' + name +'!'}
    return jsonify(response)
    


if __name__ == '__main__':
     app.run(debug=True, port=4545)