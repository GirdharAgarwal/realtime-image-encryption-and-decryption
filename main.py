from flask import Flask, render_template
import cv2
import pyautogui
from camera import VideoCamera
from deepface import DeepFace
from Crypto.Cipher import DES3
from hashlib import md5

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt/')
def encrypt():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test", cv2.WINDOW_FULLSCREEN )
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)
    
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 13:
            # ENTER pressed
            cam.release()
            cv2.imwrite("Frame.jpg",frame)
            cv2.destroyAllWindows()
            break
    file_path = 'C:/Users/GIRDHAR AGARWAL/Desktop/mini_project/Frame.jpg'
    key = "ENCRYPT"
    key_hash = md5(key.encode('ascii')).digest()
    tdes_key = DES3.adjust_key_parity(key_hash)
    cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0')

    with open(file_path, 'rb') as input_file:
        file_bytes = input_file.read()
        new_file_bytes = cipher.encrypt(file_bytes)
    with open(file_path, 'wb') as output_file:
        output_file.write(new_file_bytes)
        print('Operation Done!')
    return "bye"

@app.route('/decrypt/')
def decrypt():
    file_path = 'C:/Users/GIRDHAR AGARWAL/Desktop/mini_project/Frame.jpg'
    key = "ENCRYPT"
    key_hash = md5(key.encode('ascii')).digest()
    tdes_key = DES3.adjust_key_parity(key_hash)
    cipher = DES3.new(tdes_key, DES3.MODE_EAX, nonce=b'0')

    with open(file_path, 'rb') as input_file:
        file_bytes = input_file.read()
        new_file_bytes = cipher.decrypt(file_bytes)
    with open(file_path, 'wb') as output_file:
        output_file.write(new_file_bytes)
        print('Operation Done!')
    return "bye"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000', debug='True')