from flask import Flask, request
from config.config import SECRET_KEY
from routes.index import index_route
from routes.processing import processing_route
from socketio_app import socketio

app = Flask(__file__)
app.config["SECRET_KEY"] = SECRET_KEY

socketio.init_app(app)

@socketio.on('connect')
def handle_connect():
    socketio.emit('socket_id', {'socket_id': request.sid})

app.register_blueprint(index_route)
app.register_blueprint(processing_route)

if __name__ == "__main__":
    socketio.run(app, "localhost", debug=True)