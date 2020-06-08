import pytesseract
import cv2
import matplotlib.pyplot as plt
from PIL import Image
from flask import request
from pytesseract import Output
from werkzeug.utils import secure_filename
import base64
import os
import json
import pickle
# from BackgroundRemoval import processImage
import shutil
from TokenManagement import TokenManager


# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def get_custom_handwriting() -> list:
    fp = open("custom.hw", "rb")
    custom_hw = pickle.load(fp)
    fp.close()
    return custom_hw

def add_custom_handwriting(hw_name: str) -> list:
    fp = open("custom.hw", "rb")
    custom_hw = pickle.load(fp)
    fp.close()
    custom_hw.append(hw_name)
    with open("custom.hw", "wb") as fp:
        pickle.dump(custom_hw, fp)
        fp.close()
    return custom_hw

def createEmptyCustomHW():
    data = []
    with open("custom.hw", "wb") as f:
            pickle.dump(data, f)

def list_to_json(l: list) -> str:
    return json.dumps(l)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_image(image) -> Image:
    try:
        image = cv2.imread(image)
        return image
    except:
        return False

def get_boxes(image: Image) -> dict:
    box_raw = pytesseract.image_to_boxes(image)
    boxes = {}
    h, w, _ = image.shape
    for b in box_raw.splitlines():
        b = b.split(' ')
        char = b[0]
        x1 = int(b[1])
        y1 = h - int(b[2])
        x2 = int(b[3])
        y2 = h - int(b[4])
        boxes[char] = (x1, y1, x2, y2)
    return boxes

def extract_letters(image: Image, boxes: dict, token: str):
    tk = TokenManager()
    hw_name = tk.getTokenName(token);
    path = os.path.join('./static/trained/',hw_name)
    defaultPath = os.path.join('./static/trained/','defaultText2')
    if not os.path.exists(path):
            os.mkdir(path)
            print(hw_name, "folder created at", path)
    for i in range(32, 126):
        status=False
        try:
            if i == 96:
                continue
            char = chr(i)
            filename_t = "{}_t.png".format(i)
            if char in boxes.keys():
                #TODO
                x1,y1,x2,y2 = boxes[char]
                output = image[y1:y2, x1:x2]
                # output = processImage(letter)
                cv2.imwrite(os.path.join(path,filename_t), output)
                status=True
            else:
                source = os.path.join(defaultPath,filename_t)
                dest = os.path.join(path, filename_t)
                print("copying {} to {}".format(source, dest))
                shutil.copyfile(source,dest)
                status=False
            yield (char,status)
        except Exception as ex:
            source = os.path.join(defaultPath,filename_t)
            dest = os.path.join(path, filename_t)
            print("copying {} to {}".format(source, dest))
            shutil.copyfile(source,dest)
            yield (char,status)
    return True

def get_base64(image):
    retval, buffer = cv2.imencode(".png", image)
    png = base64.b64encode(buffer)
    return png.decode('utf-8')

def boxes_web(boxes: dict, image):
    for char in boxes:
        x1, y1, x2, y2 = boxes[char]
        cv2.rectangle(image, (x1,y1), (x2,y2), (0,255,0), 2)
    return get_base64(image)

def get_handwriting_list() -> list:
    path = os.path.join("./static/", "trained")
    output = set(sorted([dI for dI in os.listdir(path) if os.path.isdir(os.path.join(path,dI))]))
    print(output)
    print(get_custom_handwriting())
    output = output - set(get_custom_handwriting())
    return list(sorted(list(output)))
