# Install Custom Vision Service SDK
# pip install azure-cognitiveservices-vision-customvision
# Python SDK Samples https://github.com/Azure-Samples/cognitive-services-python-sdk-samples/tree/master/samples

# from web import app
#import argparse
import os
import json
#import numpy as np
#import cv2
import requests
import smartcar
#import sys
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from flask import Flask, request, Response
from flask_cors import cross_origin
from twilio.rest import Client

app = Flask(__name__)

# Set these variables based on the settings of your trained project
SAMPLE_PROJECT_NAME = "SafeTripProjectNew"
ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com"
training_endpoint = "https://southcentralus.api.cognitive.microsoft.com/customvision/v3.0/Training/"
prediction_endpoint = "https://southcentralus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/"
training_key = "24745e033ff54714ace84b9ba0268d32"
prediction_key = "4c08665e1853437eb0c9710b012fb3a7"

CLOSED_EYES = "closed"
OPEN_EYES = "opened"

filename = os.path.join(app.instance_path, 'my_folder', 'my_file.txt')

eyesflag = 1

count = 0

client = smartcar.AuthClient(
    client_id='dc343191-8dc6-4e60-bdd7-15d8a3148acd',
    client_secret='653ed077-940b-4088-92fe-053134a0ad98',
    redirect_uri='http://localhost:8000/exchange',
    scope=['read_vehicle_info', 'read_location'],
    test_mode=False,
)

acc = 'a2c005a4-a2e5-4a90-8a6c-f6af0491d8c1'


def message(id, loc):
    # Account Sid and Auth Token from twilio.com/console
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
            trainer = CustomVisionTrainingClient(training_key, endpoint=ENDPOINT)
            for proj in trainer.get_projects():
                if (proj.name == SAMPLE_PROJECT_NAME):
                    return proj
        except Exception as e:
            print(str(e))


@app.route('/data', methods=['POST', 'GET'])
@cross_origin()
def post():

    file = request.files['file']

    json_data = {"data": "open", "loc": ""}

    # Get predictor and project objects
    predictor = CustomVisionPredictionClient(prediction_key, endpoint=ENDPOINT)
    project = find_project()

    results = predictor.predict_image(project.id, file.stream.read())
    print(results.predictions)

    for prediction in results.predictions:
        print(prediction.tag_name)

        if prediction.tag_name == CLOSED_EYES:
            print ("CLOSED EYESSSS")
            if ((prediction.probability * 100) > 70):
                global count
                count += 1
                if count == 3:
                    count = 0
                    # json_data = {"data": "closed", "loc": {}}
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
                    vld = req['vehicles'][0]
                    v = smartcar.Vehicle(vld, acc)
                    print(v.location())
                    json_data = {"data": "closed", "loc": str(v.location()['data'])}
                    message(vld, v.location()['data'])
                    os.system('afplay ./alert.mp3')
                    print("hazard!")
                url = 'https://www.jsonstore.io/962b54063ad9a4019de7f1629eea83173b549ae39f2d064e1f9f724b35851731'
                headers = {'Content-Type': 'application/json'}
                requests.post(url, json=json_data, headers=headers)
            else:
                json_data = {"data": "open", "loc": ""}
                url = 'https://www.jsonstore.io/962b54063ad9a4019de7f1629eea83173b549ae39f2d064e1f9f724b35851731'
                headers = {'Content-Type': 'application/json'}
                requests.post(url, json=json_data, headers=headers)
                # global count
                count = 0
    return Response(json_data)


def run():
    app.run(debug=True, port=5001)

run()


