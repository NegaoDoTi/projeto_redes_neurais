from pathlib import Path
from uuid import uuid4
from flask import send_file, jsonify
from config.serializer import serializer
from pathlib import Path
from PIL import Image
from ultralytics import YOLO
import cv2

class ProcessingController:
    
    def __init__(self):
        
        self.model_path = Path(Path(__file__).parent.parent, "best.pt")
        
        self.upload_path = Path(Path(__file__).parent.parent, "static", "upload")
        self.upload_image_path = Path(Path(self.upload_path), "images")
        
        self.download_path = Path(Path(__file__).parent.parent, "static", "download")
        self.download_image_path = Path(Path(self.download_path), "images")
        
        self.ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        
    def allowed_file(self, filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in self.ALLOWED_EXTENSIONS
        
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
        
        return jsonify({"url" : f"http://localhost:5000/processed/image/{token}"})
        
    def render_image(self, token):
        try:
            data = serializer.loads(token)
        except:
            return jsonify({"message" : "URL invalida!"}), 404
        
        return send_file(data["image_path"])