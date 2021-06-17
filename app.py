from flask import Flask, request, jsonify
from flask_cors import CORS
from Routes.animales import animales

app = Flask(__name__)
cors = CORS(app)

app.add_url_rule('/', view_func=animales.get_animales)

if __name__ == '__main__':
    #app.run(debug=True,host='192.168.0.50', port=5000)
    app.run(debug=True, port=5000)
