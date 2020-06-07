from flask import Flask, render_template, flash, request, redirect
from TokenManagement import TokenManager
import utils
from werkzeug.utils import secure_filename
import os



app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = "SgVkYp3s6v9y$B&E)H@McQfTjWmZq4t7w!z%C*F-JaNdRgUkXp2r5u8x/A?D(G+K"
UPLOAD_FOLDER = './static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#WSGI Module
application = app
tk = TokenManager()

@app.route("/", methods=["GET"])
def home():
    handwriting_list = utils.get_handwriting_list()
    hw_json = utils.list_to_json(handwriting_list)
    return render_template('index.html', handwriting_list=hw_json)

@app.route("/custom_handwriting", methods=['GET','POST'])
def showCustomHandwritingPage():
    if request.method == 'GET':
        return render_template('custom_handwriting.html')
    form = request.form
    token = form['token']
    if not tk.checkToken(token):
        return render_template('custom_handwriting.html', msg="Invalid Token")
    print(request.files)
    if 'file' not in request.files:
        return render_template('custom_handwriting.html', msg="No file selected")
    file = request.files['file']
    if (not file) and not utils.allowed_file(file.filename):
        return render_template('custom_handwriting.html', msg="Invalid File selected")
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    # Start Training
    image = utils.load_image(path)
    if image is False:
        return render_template('custom_handwriting.html', msg="Some Error Occured with image, try again")
    boxes = utils.get_boxes(image)
    b64 = utils.boxes_web(boxes, image)
    return render_template('custom_progress.html',img=b64, token=token)

@app.route("/extract_handwriting", methods=["POST"])
def extractHandwriting():
    form = request.form
    filename = form['filename']
    token = form['token']
    correct = form['correct']
    if correct != "Yes":
        return redirect("/custom_handwriting")
    if not tk.checkToken(token):
        return "Invalid token"
    
    # Extract each letter and save it in it's folder
    image = utils.load_image(filename)
    boxes = utils.get_boxes(image)
    extract = utils.extract_letters(image,boxes,token)
    
    
@app.route("/ajax/load_token", methods=["POST"])
def load_token():
    token = request.form['token']
    if tk.checkToken(token):
        key = tk.getTokenName(token)
        return {"status":"valid","hw_name":key}
    return {"status":"invalid","hw_name":""}

if __name__ == '__main__':
    app.run(debug=True)
