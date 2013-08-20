// Additional JS functions here
$(document).ready(function() {
	console.log('document ready!')
	$('#fblogin').hide();
	$('#actulink').hide();
});


function login() {
	FB.login(function(response) {
		if (response.authResponse) {
			// connected
			console.log('logging you in!');
			testAPI();
		} else {
			// cancelled
			console.log('cancelled')
		}
	}, {
		scope : "friends_birthday,publish_actions" //This is where the sweet permission go!
	});
};

function testAPI() {
	console.log('Welcome!  Fetching your information.... ');
	FB.api('/me', function(response) {
		console.log('Good to see you, ' + response.name + '.');
	});
};

function renderLogin() {
	$('#fblogin').show();
	$('#actulink').hide();
};

function renderActuLink() {
	$('#fblogin').hide();
	$('#actulink').show();
};

window.fbAsyncInit = function() {
	
	FB.init({
		appId : '624790460881207', // App ID fbtest = 624790460881207 actuarize = 337031986416801
		channelUrl : '//www.fbtest3500.appspot.com/scripts/channel.html', // Channel File
		status : false, // check login status
		cookie : true, // enable cookies to allow the server to access the session
		xfbml : true // parse XFBML
	});
	FB.Event.subscribe('auth.authResponseChange', function(response) {
		console.log('The status of the session is: ' + response.status);
		if (response.status === 'connected') { 
		//Takes user to the FB actuarized Page!
		window.location.replace("/fbactuarized");
		} else {
			//another funciton?
		}
	});

	// Additional init code here
	FB.getLoginStatus(function(response) {
		console.log(response.status);
		if (response.status === 'connected') {
			// connected
			testAPI();
		} else if (response.status === 'not_authorized') {
			// not_authorized (here is where I should probably add some onclick events? Instead of Automatic...)
			console.log('not authorized');
			renderLogin();
		} else {
			// not_logged_in
			console.log('not logged in!');
			renderLogin();
		}
	});

};

// Load the SDK Asynchronously
( function(d) {
		var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
		if (d.getElementById(id)) {
			return;
		}
		js = d.createElement('script');
		js.id = id;
		js.async = true;
		js.src = "//connect.facebook.net/en_US/all.js";
		ref.parentNode.insertBefore(js, ref);
	}(document));
