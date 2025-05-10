from flask import Blueprint, request
from controllers.IndexController import IndexController

index_route = Blueprint("index_route", __name__, url_prefix="/")

@index_route.route("/", methods=["POST"])
def index():
    return IndexController().index(request)
