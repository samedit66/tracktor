import argparse

import cv2
from ultralytics import YOLO
import numpy as np
from tqdm import tqdm


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
progress_bar = tqdm(total=length)
while input_video.isOpened():
    success, frame = input_video.read()
    
    if not success:
        break

    results = model.track(frame, classes=args.obj_class, persist=True, verbose=False)

    # Для обрезки искомых объектов...
    boxes = results[0].boxes.xywh
    # ...создается полностью черный кадр,
    # в который будут копироваться bounding boxes найденных сущностей.
    # Поверх этого кадра будут отрисоваться сами bounding boxes.
    black_frame = np.zeros_like(frame)
    for box in boxes:
        # Необходимо скорректировать координаты: формат xywh YOLO обозначает
        # центральную координату bounding box и ширину и высоту.
        # Меняем координаты так, чтобы x и y были координатами левого верхнего угла.
        x, y, w, h = [int(c) for c in box]
        x = x - w//2
        y = y - h//2
        # Копируем из исходного кадра изображений найденного объекта.
        black_frame[y:y+h, x:x+w] = frame[y:y+h, x:x+w]
    # Отрисовываем рамку в которой описан ID сущности, имя класса и скор для данного класса.
    annotated_frame = results[0].plot(img=black_frame)

    output_video.write(annotated_frame)

    progress_bar.update(1)

progress_bar.close()

input_video.release()
output_video.release()
cv2.destroyAllWindows()