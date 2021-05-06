from flask import Flask
from controllers import front_controller as fc
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
fc.route(app)

if __name__ == "__main__":
    app.run(debug=True)
else:
    print(__name__)
