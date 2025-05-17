from flask import Blueprint, request
from controllers.ProcessingController import ProcessingController

processing_route = Blueprint("processing_route", __name__, url_prefix="/")


@processing_route.route("/processing/image", methods=["POST"])
def processing_image():
    return ProcessingController().processing_image(request)

@processing_route.route("/processed/<token>", methods=["GET"])
def processed_image(token):
    return ProcessingController().render_image(token)

@processing_route.route("/processing/video", methods=["POST"])
def processing_video():
    return ProcessingController().processing_video(request)