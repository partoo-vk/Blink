# Install Custom Vision Service SDK
# pip install azure-cognitiveservices-vision-customvision
# Python SDK Samples https://github.com/Azure-Samples/cognitive-services-python-sdk-samples/tree/master/samples

# from web import app
import argparse
import os

import json

import numpy as np
# import time
import cv2
import requests
import smartcar
# from azure.cognitiveservices.vision.customvision.training.models import ImageUrlCreateEntry
import sys
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
# from PIL import Image
from flask import Flask, request, Response
from flask_cors import cross_origin
from twilio.rest import Client
from PIL import Image

app = Flask(__name__)

# Set these variables based on the settings of your trained project
SAMPLE_PROJECT_NAME = "OpenCloseEyesOnlyEye"
ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com"
training_endpoint = "https://southcentralus.api.cognitive.microsoft.com/customvision/v2.2/Training/"
prediction_endpoint = "https://southcentralus.api.cognitive.microsoft.com/customvision/v2.0/Prediction/"
training_key = "db452ef08d47430187c98ea32d2aa6dc"
prediction_key = "eb15c0b25ec3469da4b5318693c3cdd7"

CLOSED_EYES = "Negative"
OPEN_EYES = "opened eyes"

filename = os.path.join(app.instance_path, 'my_folder', 'my_file.txt')

eyesflag = 1
count = 0
files = [f for f in os.listdir('.') if os.path.isfile(f)]
print(files)
# with open(os.path.join(app.root_path, 'access_token.json')) as json_file:
#     print("khar")
#     acc = json.load(json_file)['access_token']

client = smartcar.AuthClient(
    client_id='dc343191-8dc6-4e60-bdd7-15d8a3148acd',
    client_secret='653ed077-940b-4088-92fe-053134a0ad98',
    redirect_uri='http://localhost:8000/exchange',
    scope=['read_vehicle_info', 'read_location'],
    test_mode=False,
)

def def_parser():
    parser = argparse.ArgumentParser(description="Plot the recovery chart!")
    parser.add_argument('-a', '--access-toke', dest='a', help='access token'  , type=str, required=True)

    return parser


def parse_args(parser):
    opts = vars(parser.parse_args(sys.argv[1:]))
    return opts

# opts = parse_args(def_parser())
# acc = opts['a']

acc = 'a2c005a4-a2e5-4a90-8a6c-f6af0491d8c1'


def message(id, loc):
    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = 'AC363498a917b702d17a677bb715a4c052'
    auth_token = 'f12b59db47775c5e4437f85cd3730b83'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=f"Hello, you have been listed as an emergency contact. My smartcar ID is {id}. I feel sleepy and cannot drive. Please pick me up at: {loc}",
                         from_='+16476942899',
                         to='+16472280355'
                     )

    print(message.sid)


def find_project():
        try:
            #print("Get trainer")
            trainer = CustomVisionTrainingClient(training_key, endpoint=ENDPOINT)

            #print("get project")
            for proj in trainer.get_projects():
                if (proj.name == SAMPLE_PROJECT_NAME):
                    return proj
        except Exception as e:
            print(str(e))


@app.route('/data', methods=['POST', 'GET'])
@cross_origin()
def post():
    # print(request.data)
    # print(request.values)
    # print(request.form)
    # print(request.args)
    # print(request.get_json())
    # print(request.get_data())
    file = request.files['file']
    # file.save("/Users/elahejalalpour/Documents/GitHub/Blink/" + file.filename)

    json_data = {"data": "open", "loc": ""}

    # video_capture = cv2.VideoCapture(0)

    # Get predictor and project objects
    predictor = CustomVisionPredictionClient(prediction_key, endpoint=ENDPOINT)
    project = find_project()

    results = predictor.predict_image(project.id, file.stream.read())
    print(results.predictions)

    for prediction in results.predictions:
        print(prediction.tag_name)

        if prediction.tag_name == CLOSED_EYES:
            if ((prediction.probability * 100) > 20):
                global count
                count += 1
                if count == 3:

                    # global count
                    count = 0
                    json_data = {"data": "closed", "loc": {}}
                    with open(os.path.join(app.root_path, 'access_token.json')) as json_file:
                        js = json.load(json_file)
                        refresh = js['refresh_token']
                        acc = js['access_token']
                    try:
                        req = smartcar.get_vehicle_ids(acc)
                    except smartcar.AuthenticationException:
                            code = client.exchange_refresh_token(refresh)
                            with open(os.path.join(app.root_path, 'access_token.json'), 'w') as json_file:
                                data = {"refresh_token": code["refresh_token"],
                                        "access_token": code["access_token"]}
                                json.dump(data, json_file)

                            req = smartcar.get_vehicle_ids(code["access_token"])
                    print(req)
                    vld = req['vehicles'][0]
                    v = smartcar.Vehicle(vld, acc)
                    print(v.location())
                    # json_data = {"data": "closed", "loc": "hi"}
                    # message("hi", "loc")
                    # message(vld, v.location()['data'])
                    #request.put(json=json_data)
                    print("hazard!")
                url = 'https://www.jsonstore.io/962b54063ad9a4019de7f1629eea83173b549ae39f2d064e1f9f724b35851731'
                headers = {'Content-Type': 'application/json'}
                requests.post(url, json=json_data, headers=headers)
            else:
                json_data = {"data": "open", "loc": ""}
                url = 'https://www.jsonstore.io/962b54063ad9a4019de7f1629eea83173b549ae39f2d064e1f9f724b35851731'
                headers = {'Content-Type': 'application/json'}
                requests.post(url, json=json_data, headers=headers)
                count = 0

    return Response(json_data)


def run():
    # api.add_resource(Detection, '/data')
    app.run(debug=True, port=5001)

run()


