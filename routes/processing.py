from flask import Blueprint, request

processing_route = Blueprint("processing_route", __name__, url_prefix="/")


@processing_route.route("/processing/image", methods=["POST"])
def processing_image():
    return

@processing_route.route("/processing/video", methods=["POST"])
def processing_video():
    return