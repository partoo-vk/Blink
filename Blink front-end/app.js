var keepRunning = 1;

function change_status(ting) {
	if (ting == "open"){
	    document.getElementById("status").innerHTML = "No Hazard detected";
	    document.getElementById("status").style = "color: green;";
	}
	else if (ting == "closed") {
		document.getElementById("status").innerHTML = "STOP DRIVING";
    	document.getElementById("status").style = "color: red;";
    	keepRunning = 0;
	}
}
var BlinkApp = angular.module('BlinkApp', []);
BlinkApp.controller('BlinkApp', function($scope, $http){
    function run() {
	if(keepRunning == 1){
		take_snapshot($http);
	  $http.get("https://www.jsonstore.io/962b54063ad9a4019de7f1629eea83173b549ae39f2d064e1f9f724b35851731")
	  .success(function(data){
	    $scope.rates = data;

	    console.log(data);
	    console.log(data.result.data);
		change_status(data.result.data);
		console.log(keepRunning);

	  }
	  );
	 }
}

<!-- Code to handle taking the snapshot and displaying it locally -->
function take_snapshot($http) {

 // take snapshot and get image data
 Webcam.snap( function(data_uri) {
 	var blob = dataURLtoBlob(data_uri);
	var fd = new FormData();
	fd.append('file', blob, 'image.jpeg');
	// var req = {
	//     image: blob};
	// navigator.geolocation.getCurrentPosition(function(position) {
    // fd.append('lat', position.coords.latitude, 'location');
    // fd.append('long', position.coords.longitude, 'location');
    // req.lat = position.coords.latitude;
    // req.long = position.coords.longitude;
    // console.log(req)
    // });
	$.ajax({
      type: 'POST',
      url: 'http://localhost:5001/data',
      data: fd,
      cache: false,
      processData: false,
      contentType: false
    }).done(function(data) {
      console.log(data);
    });
	// $http.post( 'http://localhost:5001/data', fd);
    document.getElementById('results').innerHTML =
    '<img src="'+data_uri+'"/>';
  } );
}

run();
setInterval(run, 3000);

});

function convertURIToImageData(URI) {
  return new Promise(function(resolve, reject) {
    if (URI == null) return reject();
    var canvas = document.createElement('canvas'),
        context = canvas.getContext('2d'),
        image = new Image();
    image.addEventListener('load', function() {
      canvas.width = image.width;
      canvas.height = image.height;
      context.drawImage(image, 0, 0, canvas.width, canvas.height);
      resolve(context.getImageData(0, 0, canvas.width, canvas.height));
    }, false);
    image.src = URI;
  });
}

function dataURLtoBlob(dataurl) {
    var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while(n--){
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], {type:mime});
}

function geoFindMe() {

  const status = document.querySelector('#status');
  const mapLink = document.querySelector('#map-link');

  function success(position) {
    const latitude  = position.coords.latitude;
    const longitude = position.coords.longitude;

  }

  function error() {
    status.textContent = 'Unable to retrieve your location';
  }

  if (!navigator.geolocation) {
    status.textContent = 'Geolocation is not supported by your browser';
  } else {
    status.textContent = 'Locating…';
    navigator.geolocation.getCurrentPosition(success, error);
  }

}