from flask import Flask
from config.config import SECRET_KEY

app = Flask(__file__)
app.config["SECRET_KEY"] = SECRET_KEY

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)