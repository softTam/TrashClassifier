from flask import Flask, request, jsonify
from detect import localize_objects
import os
from werkzeug.utils import secure_filename
from chatgpt import solution
from classify import predict_image_classification_sample

app = Flask(__name__)

# Setting up for classification model
import base64

from google.cloud import aiplatform
from vertexai import preview
from google.cloud.aiplatform.gapic.schema import predict

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "./norse-lens-411805-d1b767e58bfa.json"

aiplatform.init(
    # your Google Cloud Project ID or number
    # environment default used is not set
    project='932924563321',

    # the Vertex AI region you will use
    # defaults to us-central1
    location='us-central1',

    # Google Cloud Storage bucket in same region as location
    # used to stage artifacts
    staging_bucket='gs://us-central1',

    # custom google.auth.credentials.Credentials
    # environment default credentials used if not set

    # credentials='./application_default_credentials.json',

    # customer managed encryption key resource name
    # will be applied to all Vertex AI resources if set

    # encryption_spec_key_name=my_encryption_key_name,

    # the name of the experiment to use to track
    # logged metrics and parameters
    experiment='my-experiment',

    # description of the experiment above
    experiment_description='my experiment description'
)

# End of classification setup


UPLOAD_FOLDER="./images"

def allowed_file(filename):
    return '.' in filename

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

        
        # response_string=localize_objects(f"./images/{filename}")
        # response_string = solution(response_string)
        
        classification_result = predict_image_classification_sample(
                                project="932924563321",
                                endpoint_id="99477215011405824",
                                location="us-central1",
                                filename=f"./images/{filename}"
                            )
        response = jsonify({'msg': classification_result})
        # response = jsonify(response_string)

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
