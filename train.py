from ultralytics import YOLO
import torch

if __name__ == '__main__':
    print("torch", torch.__version__, "cuda runtime", torch.version.cuda, "cuda available", torch.cuda.is_available())
    
    model = YOLO("yolov8n.pt")
    
    # Notice we kept epochs=200 and device=0
    result = model.train(data="merged_agri_data.yaml", epochs=200, imgsz=512, device=0) 