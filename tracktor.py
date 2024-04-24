import argparse

import cv2
from ultralytics import YOLO


parser = argparse.ArgumentParser()
parser.add_argument('video_path', type=str, help='path to video')
parser.add_argument('--class',
                    dest='obj_class',
                    type=int,
                    help='class index according to COCO 2017 dataset',
                    required=True,
                    )
args = parser.parse_args()

input_video = cv2.VideoCapture(args.video_path)
fps = input_video.get(cv2.CAP_PROP_FPS)
width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
length = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))

output_path = 'output.avi'
output_video = cv2.VideoWriter(output_path , cv2.VideoWriter_fourcc(*'MJPG'), fps, (width, height))

model = YOLO('yolov8n.pt')
while input_video.isOpened():
    success, frame = input_video.read()
    
    if not success:
        break

    results = model.predict(frame, classes=args.obj_class, verbose=False)
    annotated_frame = results[0].plot()

    output_video.write(annotated_frame)

input_video.release()
output_video.release()
cv2.destroyAllWindows()