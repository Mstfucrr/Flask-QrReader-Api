import time
from flask import Flask

app = Flask(__name__)
app.secret_key = 'super secret key'


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/qr')
def qr():
    import numpy as np
    import cv2
    from pyzbar.pyzbar import decode
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)
    i = 1;
    mydata = ''
    while i == 1:
        success, cam = cap.read()
        for barcode in decode(cam):
            mydata = barcode.data.decode('utf-8')
            print(mydata)
            pts = np.array([barcode.polygon],np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(cam,[pts],True, (0,250,150) ,5)
            pts2 = barcode.rect
            cv2.putText(cam,mydata,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,250,150),2)
            i = 0
            time.sleep(1)
        
        cv2.imshow('Result', cam)
        cv2.waitKey(1)
        if len(mydata) > 0:
            cv2.destroyAllWindows()
    return mydata


if __name__ == '__main__':
    app.run(debug=True)
    


