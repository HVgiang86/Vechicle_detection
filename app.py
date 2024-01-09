import base64
import io
import json

import socketio
from PIL import Image

from track import *

sio = socketio.Client()
sio.connect('http://127.0.0.1:5000')

# socket_server = SocketIO(app)
fileName = 'Cars Moving On Road Stock Footage - Free Download.mp4'


# define event
@sio.event
def connect():
    print("Connected to server")


@sio.event
def disconnect():
    print("Disconnected from the server")


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
    # print('base64: ', base64Img)

    return base64Img


def end_of_stream_base64():
    image_path = 'videos/endofstream.png'
    # Read the image file in binary mode
    with open(image_path, 'rb') as image_file:
        binary_data = image_file.read()
    # Encode the binary data to base64
    base64_encoded_data = base64.b64encode(binary_data)
    # Convert to a string for easier use
    base64_string = base64_encoded_data.decode('utf-8')
    return base64_string


def end_of_stream_data():
    # Emit to socket client from here

    data = {"base64Img": end_of_stream_base64(), "current_vehicle_per_fps": 0, "data_car": 0, "data_bus": 0,
            "data_truck": 0, "data_motor": len(data_motor), "fps": 0}


def detection_callback(event, result_image, current_vehicle, data_car, data_bus, data_truck, data_motor, fps):
    # print('event: ', event)
    # print('buffer: ', result_image)
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

    print(event + '\tcurrent: ' + str(len(current_vehicle)))
    print('car: ', len(data_car))

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


if __name__ == '__main__':
    start_demo_detection(fileName, 'r1_ai', detection_callback)
