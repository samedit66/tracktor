import argparse

import cv2
from ultralytics import YOLO


parser = argparse.ArgumentParser()
parser.add_argument('video_path', type=str, help='path to video')
args = parser.parse_args()

input_video = cv2.VideoCapture(args.video_path)

model = YOLO('yolov8n.pt')
while input_video.isOpened():
    success, frame = input_video.read()
    
    if not success:
        break

    # classes=15 - определяем только кошек и котов
    results = model.predict(frame, classes=15, verbose=False)
    annotated_frame = results[0].plot()

    cv2.imshow('Tracktor', annotated_frame)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

input_video.release()
cv2.destroyAllWindows()