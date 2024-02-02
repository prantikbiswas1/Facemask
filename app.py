from flask import Flask, render_template,jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from io import StringIO
import io
from PIL import Image
import cv2
import imutils
import base64
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

host = os.environ.get("HOST")
port = int(os.environ.get("PORT"))



app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

data = {
    'host' : host,
    'port' : port
}

@app.route("/")
def hello():
    return ("Hello World")


@app.route("/json")
def send_json():
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=10000)


# @socketio.on('image')
# def image(data_image):
#     sbuf = StringIO()
#     sbuf.write(data_image)

#     # decode and convert into image
#     b = io.BytesIO(base64.b64decode(data_image))
#     pimg = Image.open(b)

#     ## converting RGB to BGR, as opencv standards
#     frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

#     # Process the image frame
#     frame = imutils.resize(frame, width=500,height=375)
#     frame = cv2.flip(frame, 1)
#     imgencode = cv2.imencode('.jpg', frame)[1]


#     # base64 encode
#     stringData = base64.b64encode(imgencode).decode('utf-8')
#     b64_src = 'data:image/jpg;base64,'
#     stringData = b64_src + stringData

#     # emit the frame back
#     emit('response_back', stringData)
