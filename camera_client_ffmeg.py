import cv2
import subprocess

video_path = 'videos/test10s.mp4'
video = cv2.VideoCapture(video_path)

# RTSP URL
rtsp_port = 5001

# FFmpeg command for streaming to RTSP
command = [
    'ffmpeg',
    '-re',  # Read input at native frame rate
    '-i', video_path,  # Input file
    '-c:v', 'libx264',  # Codec: h.264
    '-preset', 'veryfast',  # Encoding speed/quality trade-off
    '-tune', 'zerolatency',  # Optimization for fast encoding and low latency
    '-b:v', '2M',  # Bitrate
    '-f', 'rtsp',  # Format is RTSP
    f"rtsp://localhost:{rtsp_port}/live.sdp"  # RTSP URL
]

# Run the FFmpeg command
subprocess.run(command)