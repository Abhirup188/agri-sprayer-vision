from ultralytics import YOLO
import cv2
import cvzone
import math
import torch

print("torch", torch.__version__, "cuda runtime", torch.version.cuda, "cuda available", torch.cuda.is_available())

cap = cv2.VideoCapture("videos/plant_infection.mp4") 
# cap = cv2.VideoCapture("videos/healthy plant.mp4") 
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
                status = "HEALTHY"
                action = "NO ACTION"
                color = (0,255,0)
            else:
                threat_detected = True
                if area_percentage < 5.0:
                    status = "MILD INFECTION"
                    action = "Short Spray (0.5s)"
                    color = (0, 165, 255) 
                else:
                    status = "SEVERE INFECTION"
                    action = "Long Spray (2.0s)"
                    color = (0, 0, 255) 

            cvzone.cornerRect(img, (x1, y1, w, h), l=15, t=2, colorR=color, colorC=color)
            label = f"{status}: {detected_class} ({conf})"
            cvzone.putTextRect(img, label, (max(0, x1), max(35, y1 - 10)), scale=0.8, thickness=1, colorR=color)
            
            cvzone.putTextRect(img, action, (max(0, x1), max(65, y1 + h + 20)), scale=0.8, thickness=1, colorR=(50, 50, 50))

    if not threat_detected:
        cvzone.putTextRect(img, "SYSTEM STATUS: HEALTHY ZONE - NO ACTION REQUIRED", 
                           (20, 40), scale=1.5, thickness=2, colorR=(0, 200, 0), colorT=(255,255,255))
    # else:
    #     cvzone.putTextRect(img, "SYSTEM STATUS: THREAT ENGAGED - SPRAYING", 
    #                        (20, 40), scale=1.5, thickness=2, colorR=(0, 0, 255), colorT=(255,255,255))

    cv2.imshow("SIH Smart Sprayer Vision", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()