import base64
import io
import json
import threading

import socketio
from PIL import Image

from track import *

sio = socketio.Client()


# define event
@sio.event
def connect():
    print("Connected to server")


@sio.event
def disconnect():
    print("Disconnected from the server")


# socket_server = SocketIO(app)
fileName1 = 'Cars Moving On Road Stock Footage - Free Download.mp4'
fileName2 = 'Cars Moving On Road Stock Footage - Free Download.mp4'
fileName3 = 'Cars Moving On Road Stock Footage - Free Download.mp4'
fileName4 = 'Cars Moving On Road Stock Footage - Free Download.mp4'


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


def thread_function(fileName, event):
    start_demo_detection(fileName, event, detection_callback)


def detection_callback(event, result_image, current_vehicle, data_car, data_bus, data_truck, data_motor, fps):
    base64Img = handleImg(result_image)
    # print("Callback")
    # print('base64Img: ', base64Img)
    # print('Data car: ', data_car)
    # print('Data Bus: ', data_bus)
    # print('Data Truck: ', data_truck)
    # print('Data motor: ', data_motor)
    # print('FPS: ', fps)

    # Emit to socket client from here
    data = {"base64Img": base64Img, "current_vehicle_per_fps": len(current_vehicle), "data_car": len(data_car),
            "data_bus": len(data_bus), "data_truck": len(data_truck), "data_motor": len(data_motor), "fps": fps}

    json_string = json.dumps(data)
    sio.emit(event, json_string)


def start_demo_detection(fileName, event, result_callback):
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
        detect(opt, line, assigned_class_id, event, result_callback)


sio.connect('http://127.0.0.1:5000')

if __name__ == '__main__':
    if sio.connected:
        thread1 = threading.Thread(target=thread_function, args=(f"{fileName1}", "r1_ai"))
        thread1.start()

        thread2 = threading.Thread(target=thread_function, args=(f"{fileName2}", "r2_ai"))
        thread2.start()

        thread3 = threading.Thread(target=thread_function, args=(f"{fileName3}", "r3_ai"))
        thread3.start()

        thread4 = threading.Thread(target=thread_function, args=(f"{fileName4}", "r4_ai"))
        thread4.start()
    else:
        print("Not connected to socket server")
