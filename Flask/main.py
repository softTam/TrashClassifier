from flask import Flask, request, jsonify
from detect import localize_objects
import os
from werkzeug.utils import secure_filename
from chatgpt import solution
app = Flask(__name__)


UPLOAD_FOLDER="./images"


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/media/upload', methods = ['POST'])
def upload_media():
    if 'file' not in request.files:
        return jsonify({'error':'media not provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error':'no file selected'}), 400
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        response_string=localize_objects(f"./images/{filename}")
        response_string = solution(response_string)

        # response = jsonify({'msg': response_string})
        response = jsonify(response_string)

        os.remove(f'./images/{filename}')
        return response
    return jsonify({'error':'no file exisited'}), 400


    
@app.route('/')
def hello():
    url=localize_objects("./images/banana.jpeg")
    return jsonify({'say' : url})
    # return "Hello"
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
