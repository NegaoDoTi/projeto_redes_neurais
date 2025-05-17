from flask import Flask
from config.config import SECRET_KEY
from routes.index import index_route
from routes.processing import processing_route

app = Flask(__file__)
app.config["SECRET_KEY"] = SECRET_KEY

app.register_blueprint(index_route)
app.register_blueprint(processing_route)

if __name__ == "__main__":
    app.run("localhost", port=5000, debug=True)