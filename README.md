# Blink
Impaired driving detection system. 

# Inspiration
Our team was inspired to find a solution for safer driving after considering the recent legalization of marijuana. Being impaired due to being high, drunk or tired is a very pertinent issue. Impaired driving not only puts the driver at risk but also risks the lives of everyone else on the road. If a driver was to be impaired and remain unresponsive behind the wheel, they would most likely cause an accident on the road.
# What it does
Blink uses Microsoft's custom vision AI trained with photos of open and closed eyes. With a webcam, companies such as Uber, Lyft and Taxis can have service which monitor's their drivers (specifically whether they become impaired/unresponsive) if they drive a smart car. When Blink detects that the user's eyes have been closed for 5s, the system issues an alert using Twilio. Immediately the latitude and longitude are forwarded to an emergency contact of the driver, telling them the ID of the car in distress and the latitude and longitude of the car.
# How we built it
We are using Python and flask as the backend and angularjs as the front end. We used Azure computevision to train a model on open and closed eyes and then used that model to detect if the driver has fallen asleep by computing the amount of time their eyes are closed. We build a flask rest API using which the frontend predicts whether the driver has closed their eyes. we are using frames from the video captured by the webcam and detect closed eyes. Then we use the smartcar API to find the location of the smartcar and using twilio's SMS API we notify the driver's first responders and even the nearest police station. The frontend is developed by javascript with angular to parse json files from a jsonstored server with the info about the status of the driver, The status is displayed on the webpage by DOM manipulation.

