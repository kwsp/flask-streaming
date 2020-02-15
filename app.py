#!/usr/bin/env python
import time
from importlib import import_module
import os
from flask import Flask, render_template, Response

# import camera driver
if os.environ.get("CAMERA"):
    Camera = import_module("camera_" + os.environ["CAMERA"]).Camera
else:
    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route("/")
@app.route("/stream")
def index():
    """Video streaming home page."""
    return render_template("index.html")


user_count = 0


def gen(camera):
    """Video streaming generator function."""
    global user_count
    user_count += 1
    # t = time.time()
    try:
        while True:
            frame = camera.get_frame()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

            temp = time.time()
            # fps = 1 / (temp - t)
            # print("FPS: {:.2f}, number of users: {}".format(fps, user_count))
            # t = temp
    except GeneratorExit:
        user_count -= 1


@app.route("/stream/video_feed")
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
