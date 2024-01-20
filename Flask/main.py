from flask import Flask, request, jsonify
from detect import localize_objects
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)


UPLOAD_FOLDER="./images"

ALLOWED_EXTENSIONS = set(['txt','pdf','png', 'jpg','jpeg','gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/media/upload', methods = ['POST'])
def upload_media():
    if 'file' not in request.files:
        return jsonify({'error':'media not provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error':'no file selected'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    response=localize_objects("./images/1.jpeg")
    return jsonify({'msg': response})


    
@app.route('/')
def hello():
    url=localize_objects("./images/banana.jpeg")
    return url
    # return "Hello"
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
