from flask import render_template

class  IndexController:
    
    def index(self):
        return render_template("index.html")