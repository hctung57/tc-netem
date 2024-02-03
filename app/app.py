import os
import threading
import time
from torch import hub
from cv2 import VideoCapture
from flask import Flask

app = Flask(__name__)
model = hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)

@app.route('/api/stream/<int:time>', methods=['GET'])
def handle_streaming_thread_init(time):
    time_to_detect = time
    try:
        threading.Thread(target=detect_streaming, args=(
            "./cctv.mp4",time_to_detect,)).start()
    except:
        print("error")
    return 'OK', 200


def detect_streaming(path: str, time_to_detect: int):
    cap = VideoCapture(path)
    start_time = time.monotonic()
    frame_number = 0
    while (True):
        ret, frame = cap.read()
        if ret == True:
            frame_number += 1
            print("** HANDLE FRAME NUMBER : {}\n***TIMESTAMP: {}".format(
                frame_number,time.strftime("%Y%m%d-%H%M%S")))
            print("RESULTS:")
            results = model(frame)
            results.print()
            print(results.pandas().xyxy[0])
            print()        
            if time.monotonic() - start_time > time_to_detect:
                break
    cap.release()
    return

#using Gunicorn not running 
if __name__ == '__main__':
#    model = hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
