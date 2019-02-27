# Install Custom Vision Service SDK
# pip install azure-cognitiveservices-vision-customvision
# Python SDK Samples https://github.com/Azure-Samples/cognitive-services-python-sdk-samples/tree/master/samples

# from web import app
import numpy as np
# import time
import cv2
import requests
import smartcar
# from azure.cognitiveservices.vision.customvision.training.models import ImageUrlCreateEntry
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
# from PIL import Image
from flask import Flask, request, Response
from flask_cors import cross_origin
from twilio.rest import Client
from PIL import Image

app = Flask(__name__)
# api = Api(app)
# parser = reqparse.RequestParser()
# parser.add_argument('image', type=str)

# parser.add_argument('function', type=dict)
# parser.add_argument('position')

# Set these variables based on the settings of your trained project
SAMPLE_PROJECT_NAME = "OpenCloseEyesOnlyEye"
ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com"
training_endpoint = "https://southcentralus.api.cognitive.microsoft.com/customvision/v2.2/Training/"
prediction_endpoint = "https://southcentralus.api.cognitive.microsoft.com/customvision/v2.0/Prediction/"
training_key = "68ea975fad67401895761b406a6b3130"
prediction_key = "47ca21dcc8d344ef9762ad3a1e3c5f3b"

CLOSED_EYES = "Negative"
OPEN_EYES = "opened eyes"

eyesflag = 1
count = 0


def message(id, loc):
        # Download the helper library from https://www.twilio.com/docs/python/install


    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = 'AC1df7f15bdc28b034b5305877e9db73d0'
    auth_token = '8bf146a8c8d76cd51544c85ca9f49e92'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=f"Hello, you have been listed as an emergency contact. My smartcar ID is {id}. I feel sleepy and cannot drive. Please pick me up at: {loc}",
                         from_='+14388004097',
                         to='+16475265284'
                     )

    print(message.sid)
    OUTPUT = {
      "account_sid": "AC1df7f15bdc28b034b5305877e9db73d0",
      "api_version": "2010-04-01",
      "body": "Lets see if this works.",
      "date_created": "Thu, 30 Jul 2015 20:12:31 +0000",
      "date_sent": "Thu, 30 Jul 2015 20:12:33 +0000",
      "date_updated": "Thu, 30 Jul 2015 20:12:33 +0000",
      "direction": "outbound-api",
      "error_code": None,
      "error_message": None,
      "from": "+14388004097",
      "messaging_service_sid": "MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
      "num_media": "0",
      "num_segments": "1",
      "price": -0.00750,
      "price_unit": "USD",
      "sid": "MMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
      "status": "sent",
      "subresource_uris": {
        "media": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages/SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Media.json"
      },
      "to": "+16475265284",
      "uri": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages/SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.json"
    }


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


# class Detection(Resource):
    #global count
    # count = 0

    # def get(self):
    #     pass

@app.route('/data', methods=['POST'])
@cross_origin()
def post():
    print(request.files['file'])
    file = request.files['file']
    file.save("/Users/elahejalalpour/Documents/GitHub/Blink/" + file.filename)
    # convert string of image data to uint8
    # nparr = np.fromstring(r.data, np.uint8)
    # print(len(nparr))
    # img = Image.fromarray(nparr.reshape(28, 28), 'L')

    # decode image
    # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # print(img)
    # with open("/Users/elahejalalpour/Documents/GitHub/Blink/color_img.jpeg", 'wb') as file:
    #     file.write(r.data)
    #
    json_data = {"data": "open", "loc": ""}

    # video_capture = cv2.VideoCapture(0)

    # Get predictor and project objects
    predictor = CustomVisionPredictionClient(prediction_key, endpoint=ENDPOINT)
    project = find_project()
    print('here')
    # img = Image.fromarray(nparr, 'RGB')


    # ret, frame = video_capture.read()
    #print (ret)
    # cv2.imwrite('/Users/elahejalalpour/Documents/GitHub/Blink/color_img.jpeg', img)
    #cv2.imshow('Video', frame)
    try:
        with open('/Users/elahejalalpour/Documents/GitHub/Blink/image.jpeg', mode="rb") as test_data:
            results = predictor.predict_image(project.id, test_data)

    except Exception as e:
        print(str(e))
        input()
    # Display the results.
    for prediction in results.predictions:
        #print(prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100))

        if prediction.tag_name == CLOSED_EYES:
            if ((prediction.probability * 100) > 0.01):
                global count
                count += 1
                if count == 1:

                    # global count
                    count = 0

                    acc = '66ae978d-d815-4f75-8fe0-fc765dc5b829'
                    # req = smartcar.get_vehicle_ids(acc)
                    # vld = req['vehicles'][0]
                    # v = smartcar.Vehicle(vld, acc)
                    # print(v.location())
                    # json_data = {"data": "closed", "loc": v.location()['data']}
                    json_data = {"data": "closed", "loc": "hi"}
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

            #send_main(SRC, DST, "!!!")
        # else:
        #     json_data = {"data":"allgood", "loc":""}
        #     #global count
        #     #count = 0

        # input()
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
    # video_capture.release()
    # cv2.destroyAllWindows()

    return Response(json_data)


def run():
    # api.add_resource(Detection, '/data')
    app.run(debug=True, port=5001)

# if __name__ == '__main__':
    # global count
count = 0
run()


