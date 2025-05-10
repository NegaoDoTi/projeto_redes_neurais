from pathlib import Path
from uuid import uuid4

class ProcessingController:
    
    def __init__(self):
        self.upload_path = Path(Path(__file__).parent.parent, "static", "upload")
        self.upload_videos_path = Path(Path(self.upload_path), "videos")
        self.upload_images_path = Path(Path(self.upload_path), "images")
        
        self.download_path = Path(Path(__file__).parent.parent, "static", "download")
        self.download_image_path = Path(Path(self.download_path), "images")
        self.download_videos_path = Path(Path(self.download_path), "videos")
        
    def processing_image(self, req):
        
        id_image = str(uuid4())
        
    def processing_video(self, req):
        
        id_video = str(uuid4())
        
        