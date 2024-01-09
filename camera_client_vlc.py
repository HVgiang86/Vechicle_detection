import subprocess

# Configuration for your RTSP server
rtsp_port = "8554"
input_stream = "path/to/your/video.mp4"  # Replace with your video source

# VLC command to start the RTSP server
command = [
    "cvlc",  # Command-line VLC
    input_stream,
    "--sout", f"#rtp{{sdp=rtsp://:{rtsp_port}/stream}}",
    "--no-sout-all",
    "--sout-keep"
]

# Run the command
subprocess.run(command)
