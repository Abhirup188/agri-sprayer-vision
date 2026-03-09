from ultralytics import YOLO
import cv2
import cvzone
import math
import torch

print("torch", torch.__version__, "cuda runtime", torch.version.cuda, "cuda available", torch.cuda.is_available())

# cap = cv2.VideoCapture("videos/plant_infection.mp4") 
cap = cv2.VideoCapture("videos/healthy plant.mp4") 
MODEL_PATH = "runs/detect/train3/weights/best.pt" 

model = YOLO(MODEL_PATH)

classnames = [
    "HEALTHY CROP", "weed", "ants", "bees", "beetles", "caterpillars", 
    "earthworms", "earwigs", "grasshoppers", "moths", "slugs", 
    "snails", "wasps", "weevils"
]

while True:
    success, img = cap.read()
    if not success:
        print("Video ended.")
        break

    results = model(img, stream=True)
    
    threat_detected = False 

    for r in results:
        boxes = r.boxes
        for box in boxes:
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            detected_class = classnames[cls]

            if cls == 0: 
        
                if conf < 0.30: 
                    continue
            else:
                
                if conf < 0.60: 
                    continue
                threat_detected = True 

            x1, y1, x2, y2 = int(box.xyxy[0][0]), int(box.xyxy[0][1]), int(box.xyxy[0][2]), int(box.xyxy[0][3])
            w, h = x2 - x1, y2 - y1

            bbox_area = w * h
            frame_area = img.shape[0] * img.shape[1]
            area_percentage = (bbox_area / frame_area) * 100

            if cls == 0:
                action = "SAFE (No Spray)"
                color = (255, 0, 0) 
            else:
                if area_percentage < 5.0:
                    action = "MILD (Short Spray 0.5s)"
                    color = (0, 165, 255) 
                else:
                    action = "SEVERE (Long Spray 2.0s)"
                    color = (0, 0, 255) 

            cvzone.cornerRect(img, (x1, y1, w, h), l=15, t=2, colorR=color, colorC=color)
            label = f"{detected_class} {conf} | {action}"
            cvzone.putTextRect(img, label, (max(0, x1), max(35, y1 - 10)), scale=1, thickness=1, colorR=color)

    if not threat_detected:
        cvzone.putTextRect(img, "SYSTEM STATUS: HEALTHY ZONE - NO ACTION REQUIRED", 
                           (20, 40), scale=1.5, thickness=2, colorR=(0, 200, 0), colorT=(255,255,255))
    else:
        cvzone.putTextRect(img, "SYSTEM STATUS: THREAT ENGAGED - SPRAYING", 
                           (20, 40), scale=1.5, thickness=2, colorR=(0, 0, 255), colorT=(255,255,255))

    cv2.imshow("SIH Smart Sprayer Vision", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()