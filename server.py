import json
import time
import io
import torch
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from track import *
from flask_cors import CORS
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, cors_allowed_origins='*')

# socketio = SocketIO(app)
fileName = 'one_lane_traffic_stop.mp4'

@socketio.on('send_image')
def handle_my_custom_event(data):
    print("calling socket")
    emit('base64Image', data)

def handleImg(img):
    im = Image.fromarray(img)
    # image_path = './resultStream/your_file.jpeg'
    
    # image_path = os.path.splitext(image_path)[0]

    # new_path = image_path + str(time.localtime()) + '.jpeg'
    # im.save(new_path)

    # with open(new_path, 'rb') as f:
    image_stream = io.BytesIO()
    im.save(image_stream, format='JPEG')

    image_stream.seek(0)
    image_bytes = image_stream.read()
        
    base64Img = base64.b64encode(image_bytes).decode('utf-8')

    return base64Img


@socketio.on('start')
def handle_my_custom_event(data):
    print("calling start demo")
    start_demo_detection(fileName, detection_callback)
    print("done detection")

def detection_callback(result_image, current_vehicle, data_car, data_bus, data_truck, data_motor, fps):
    
    base64Img = handleImg(result_image)
    # print("Callback")
    # print('base64Img: ', base64Img)
    # print('Data car: ', data_car)
    # print('Data Bus: ', data_bus)
    # print('Data Truck: ', data_truck)
    # print('Data motor: ', data_motor)
    # print('FPS: ', fps)

    # Emit to socket client from here
    data = {
        "base64Img": base64Img,
        "current_vehicle_per_fps": len(current_vehicle),
        "data_car": len(data_car),
        "data_bus": len(data_bus),
        "data_truck": len(data_truck),
        "data_motor": len(data_motor),
        "fps": fps
    }

    json_string = json.dumps(data)
    emit('update_result', json_string)


def start_demo_detection(fileName, result_callback):
    # Start
    # custom class
    assigned_class_id = [0, 1, 2, 3]
    # [0,1,2,3] = ['car', 'motorcycle', 'truck', 'bus']

    # setting hyperparameter
    confidence = 0.5  # confidence, from 0.0 -> 1.0, default 0.5
    line = 0.6  # Line position: from 0.0 -> 1.0, #default 0.6

    reset()
    model_path = 'models/best_new.pt'
    opt = parse_opt(model_path=model_path)
    opt.conf_thres = confidence
    opt.source = f'videos/{fileName}'

    print('Detection Started')
    with torch.no_grad():
        detect(opt, line, assigned_class_id, result_callback)

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=5000)

