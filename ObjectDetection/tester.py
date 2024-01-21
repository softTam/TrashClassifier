# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START aiplatform_predict_image_classification_sample]
import base64

from google.cloud import aiplatform
from vertexai import preview
from google.cloud.aiplatform.gapic.schema import predict
import os

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


def predict_image_classification_sample(
    project: str,
    endpoint_id: str,
    filename: str,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    with open(filename, "rb") as f:
        file_content = f.read()

    # The format of each instance should conform to the deployed model's prediction input schema.
    encoded_content = base64.b64encode(file_content).decode("utf-8")
    instance = predict.instance.ImageClassificationPredictionInstance(
        content=encoded_content,
    ).to_value()
    instances = [instance]
    # See gs://google-cloud-aiplatform/schema/predict/params/image_classification_1.0.0.yaml for the format of the parameters.
    parameters = predict.params.ImageClassificationPredictionParams(
        confidence_threshold=0.5,
        max_predictions=5,
    ).to_value()
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    # print("response")
    # print(" deployed_model_id:", response.deployed_model_id)
    # See gs://google-cloud-aiplatform/schema/predict/prediction/image_classification_1.0.0.yaml for the format of the predictions.
    predictions = response.predictions

    dictionary = dict(predictions[0])
    return dictionary["displayNames"][0].strip('\'')

    # print(dictionary["displayNames"][0].strip('\''))
    # for d in dictionary:
    #     print(d)
    #     print(dictionary[d])
    # for prediction in predictions:
    #     print(" prediction:", dict(prediction))


# [END aiplatform_predict_image_classification_sample]
        
result = predict_image_classification_sample(
    project="932924563321",
    endpoint_id="99477215011405824",
    location="us-central1",
    filename="plasticbottle.jpeg.jpg"
)

print(result)
