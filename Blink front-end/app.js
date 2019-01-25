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
		$http.get('http://localhost:5000/');

	  $http.get("https://www.jsonstore.io/962b54063ad9a4019de7f1629eea83173b549ae39f2d064e1f9f724b35851731")
	  .success(function(data){
	    $scope.rates = data;

	    console.log(data);
	    console.log(data.result.data);
		change_status(data.result.data);
		console.log(keepRunning);

	  });
	 }
}

run();
setInterval(run, 3000);

});