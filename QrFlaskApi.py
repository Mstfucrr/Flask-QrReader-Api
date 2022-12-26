from flask import Flask, render_template, request, Response
import numpy as np
import cv2
from pyzbar.pyzbar import decode
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont

global capture,rec_frame,result, switch, rec, out 
capture=0
switch=1
rec=0
result=''

#make shots directory to save pics

#Load pretrained face detection model    

#instatiate flask app  
app = Flask(__name__, template_folder='./templates')
CORS(app)
camera = cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame
    while True:
        success, frame = camera.read() 
        if success:            
            cv2.rectangle(frame,(0,0),(frame.shape[1],80),(0,0,0),-1)
            for barcode in decode(frame):
                global result
                result = barcode.data.decode('utf-8')
                pil_im = Image.fromarray(frame)
                draw = ImageDraw.Draw(pil_im)
                font = ImageFont.truetype("arial.ttf", 40)
                draw.text((60, 20), result, font=font, fill=(0, 250, 150))
                frame = np.array(pil_im)
                pts = np.array([barcode.polygon],np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.polylines(frame,[pts],True, (0,250,150) ,5)
            try:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
            cv2.waitKey(1)


        else:
            pass
   
@app.route('/video_feed',methods=['POST','GET'])
def video_feed():
    global camera,result
    camera = cv2.VideoCapture(0)
    return Response( gen_frames() , mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST'])
def tasks():
    response=''
    global switch,camera
    if request.method == 'POST':
        camera.release()
        cv2.destroyAllWindows()
        global result
        if result:
            response = result
            result = ''
            print(response)
            return {'response': response}
        else:
            return {'response': 'No QR code detected'}


if __name__ == '__main__':
    app.run(debug=True,port=3500)
    
camera.release()
cv2.destroyAllWindows() 