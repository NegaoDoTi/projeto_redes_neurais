from flask import render_template
from config.config import TOKEN

class  IndexController:
    
    def index(self, req):
        return render_template("index.html", token=TOKEN)