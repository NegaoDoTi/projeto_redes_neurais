from flask import Blueprint
from controllers.IndexController import IndexController

index_route = Blueprint("index_route", __name__, url_prefix="/")

@index_route.route("/", methods=["GET"])
def index():
    return IndexController().index()
