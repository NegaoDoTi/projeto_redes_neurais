from pathlib import Path
from uuid import uuid4
from flask import send_file, jsonify
from config.serializer import serializer
from pathlib import Path
from PIL import Image
from ultralytics import YOLO
import cv2
from moviepy import VideoFileClip
from socketio_app import socketio

class ProcessingController:
    
    def __init__(self):
        
        self.model_path = Path(Path(__file__).parent.parent, "best.pt")
        
        self.upload_path = Path(Path(__file__).parent.parent, "static", "upload")
        self.upload_image_path = Path(Path(self.upload_path), "images")
        self.upload_video_path = Path(Path(self.upload_path), "videos")
        
        self.download_path = Path(Path(__file__).parent.parent, "static", "download")
        self.download_image_path = Path(Path(self.download_path), "images")
        self.download_video_path = Path(Path(self.download_path), "videos")
        
        self.ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        self.ALLOWED_EXTENSIONS_VIDEO = {'mp4', 'avi', 'mov', 'mpeg', "wmv", "mkv"}
        
    def allowed_file(self, filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in self.ALLOWED_EXTENSIONS
    
    def allowed_file_video(self, filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in self.ALLOWED_EXTENSIONS_VIDEO
    
    def is_valid_video(self, filepath:str) -> bool:
        try:
            video = VideoFileClip(filepath)
            
            duration = video.duration
            
            video.close()
            
            return duration > 0
        except:
            return False
        
    def processing_image(self, req):
        
        if "image" not in req.files:
            return jsonify({"message" : "Nenhum arquivo de imagem enviado"}), 400
        
        image = req.files["image"]
        
        if image.filename == "":
            return jsonify({"message" : "Nenhum arquivo selecionado"}), 400
        
        if not self.allowed_file(image.filename):
            return jsonify({"message" : "Extensão do arquivo não é permitida"}), 400
        
        try:
            img = Image.open(image.stream)
            
            img.verify()
        except:
            return jsonify({"message" : "O binario do arquivo não é de uma imagem!"})    
        
        image_id = str(uuid4())
        
        upload_path_image = f"{self.upload_image_path}/{image_id}.{image.content_type.split('/')[-1]}"
        
        image.seek(0)
        image.save(upload_path_image)
        
        final_path_image = f"{self.download_image_path}/{image_id}.{image.content_type.split('/')[-1]}"
        
        model = YOLO(f"{self.model_path}")
        
        result = model.predict(source=upload_path_image, save_txt=False, save_crop=False)
        
        for r in result:
            img_bgr = r.plot()
            
            cv2.imwrite(final_path_image, img_bgr)
        
        data = {"image_path" : f"{final_path_image}"}
        
        token = serializer.dumps(data)
        
        return jsonify({"url" : f"http://localhost:5000/processed/{token}"})
    
    def processing_video(self, req):
        if "video" not in req.files:
            return jsonify({"message" : "Nenhum arquivo de imagem encontrado no formulario!"}), 400
        
        video = req.files["video"]

        if video.filename == "":
            return jsonify({"message" : "Nenhum video selecionado"}), 400
        
        if not self.allowed_file_video(video.filename):
            return jsonify({"message" : "A extensão deste arquivo de video não é suportada"}), 400
        
        video_id = str(uuid4())
        
        final_path_video = Path(f"{self.upload_video_path}/{video_id}.{video.content_type.split('/')[-1]}")
        
        video.seek(0)
        video.save(str(final_path_video))
        
        if not self.is_valid_video(final_path_video):
            final_path_video.unlink()
            return jsonify({"message" : "O binario do video enviado não é realmente de um video!"}), 400
        
        socket_id = req.args.get('socket_id')
        if socket_id:
            socketio.start_background_task(self.finaly_processing_video, final_path_video, video_id, video.content_type.split('/')[-1], socket_id)
            return jsonify({"message" : "Video enviado e em processamento"}), 201
        else:
            return jsonify({"message" : "Id do socket esta ausente"}), 400

    def finaly_processing_video(self, final_path_video:str, video_id:str, extension_video:str, socket_id):
        model = YOLO(f"{self.model_path}")
        
        cap = cv2.VideoCapture(final_path_video)
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        video_output_path = Path(f"{self.download_video_path}/{video_id}.{extension_video}")
        
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        
        out = cv2.VideoWriter(str(video_output_path), fourcc, fps, (width, height))
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            results = model.predict(source=frame, save=False, conf=0.25, verbose=False)
            
            annotated_frame = results[0].plot()
            
            out.write(annotated_frame)
            
        cap.release()
        out.release()
        
        data = {
            "video_path" : str(video_output_path)
        }
        
        token = serializer.dumps(data)
        
        socketio.emit(
            "video_processed",
            {"url" : f"http://localhost:5000/processed/{token}"},
            to=socket_id
        )
        
    def render_image(self, token):
        try:
            data = serializer.loads(token)
        except:
            return jsonify({"message" : "URL invalida!"}), 404
        
        try:
            return send_file(data["image_path"])
        except:
            return send_file(data["video_path"])