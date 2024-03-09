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

from keras.models import load_model

model = load_model('face_mask.h5')

def draw_label(img,text,pos,bg_color):
    text_size = cv2.getTextSize(text,cv2.FONT_HERSHEY_SIMPLEX,1,cv2.FILLED)

    end_x = pos[0] + text_size[0][0] + 2
    end_y = pos[1] + text_size[0][1] - 2

    cv2.rectangle(img,(0,0),(end_x,end_y),bg_color,cv2.FILLED)
    cv2.putText(img,text,pos,cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1,cv2.LINE_AA)

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


@app.route("/json")
def send_json():
    return jsonify(data)

@socketio.on('image')
def image(data_image):
    sbuf = StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)
    


    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
    
    #frames are read using imread in cv2 in model and is same as frame
    #frame = imread

    frame = cv2.resize(frame,(224,224))
   
    frame = frame[:, :, :3]
    
    y_pred = model.predict(frame.reshape(1,224,224,3))
    if y_pred>=0.5:
        draw_label(frame,'No Mask',(30,30),(0,0,255))
    else:
        draw_label(frame,'Mask',(30,30),(0,255,0))



    # Process the image frame
    frame = imutils.resize(frame, width=500,height=375)
    imgencode = cv2.imencode('.jpg', frame)[1]


    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData

    # emit the frame back
    emit('response_back', stringData)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1')
