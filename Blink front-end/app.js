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

function take_snapshot($http) {

 Webcam.snap( function(data_uri) {
 	var blob = dataURLtoBlob(data_uri);
	var fd = new FormData();
	fd.append('file', blob, 'image.jpeg');
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
    document.getElementById('results').innerHTML =
    '<img src="'+data_uri+'"/>';
  } );
}

run();
setInterval(run, 2000);
});

function dataURLtoBlob(dataurl) {
    var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while(n--){
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], {type:mime});
}
