import torch
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from track import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('send_image')
def handle_my_custom_event(data):
    print("calling socket")
    emit('base64Image', data)

@socketio.on('update_result')
def handle_my_custom_event(data):
    print("calling socket")
    emit('base64Image', data)


fileName = 'test10s.mp4'

@socketio.on('start')
def handle_my_custom_event(data):
    print("calling start demo")
    start_demo_detection(fileName)
    print("done detection")


def start_demo_detection(fileName):
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
        detect(opt, line, assigned_class_id)

if __name__ == '__main__':
    socketio.run(app, port=5000)

