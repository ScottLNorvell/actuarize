// Additional JS functions here

function login(url) {
	FB.login(function(response) {
		if (response.authResponse) {
			// connected
			//console.log('logging you in!');
			//testAPI();
			renderStatusBox(action1);
			//window.location.replace(url);
		} else {
			// cancelled
			//console.log('cancelled')
			window.location.replace('/act');
		}
	}, {
		scope : "friends_birthday,publish_actions" //This is where the sweet permission go!
	});
};

function action1() {
	var url = $('button').attr('data-url');
	//alert('gonna go to the url: ' + url)
	//login(url);
	window.location.replace(url);
};

function renderStatusBox(action) {
	console.log("I'm in the Function Render Status Box!");
	console.log(action)
	var url = '/status-lightbox';
	$.ajax({
		url : url,
		method : 'GET',
		dataType : 'html',
		success : function(html) {
			//console.log('action= ' + action.toString());
			$("#lightbox-holder").append(html);

			$('#lightbox').fadeIn(500);
			$("#lightbox-panel").fadeIn({
				duration : 500,
				complete : progHappens
			});
			// var action is the action to be performed
			setTimeout(action, 600)
			console.log('timer set')
		}
	});

};

//Renders the progress bar and all the silly animations once its all faded in!
function progHappens() {
	var progressbar = $("#progressbar"), progressLabel = $(".progress-label");
	var pos = 0;
	var waitProg = 10;
	var waitLabel = 2000;
	var messages = ['Complete!', 'Wait, why is this still going on?', "I can't deal with this", "Complete!", "Just kidding!", "Where's my Page?", "This stopped being funny..."];
	var limit = messages.length;

	function progress() {
		var val = progressbar.progressbar("value") || 0;

		progressbar.progressbar("value", val + 1);
		//console.log('val changed before if')

		if (val < 99) {
			setTimeout(progress, waitProg);
			//console.log('Timeout set inside if')
		}
		waitProg += 3
	}

	function labelCycler() {

		//console.log('pos = ' + pos.toString() + ' --- before the cycle');

		progressLabel.text(messages[pos]);
		setTimeout(labelCycler, waitLabel);
		pos = (pos + 1) % limit;
		waitLabel += 250
		//console.log('pos = ' + pos.toString() + ' --- after the cycle');
		return

	}

	// grabs progress bar and label
	//console.log('fadeToggle Complete');

	progressbar.progressbar({
		value : false,
		change : function() {
			progressLabel.text(progressbar.progressbar("value") + "%");
		},
		complete : labelCycler
		//function() {setInterval(labelCycler, 1000)}
	});
	//console.log('progressbar set')

	setTimeout(progress, 1000);
	//console.log('progress timeout set')
};

function testAPI() {
	console.log('Welcome!  Fetching your information.... ');
	FB.api('/me', function(response) {
		console.log('Good to see you, ' + response.name + '.');
	});
};

window.fbAsyncInit = function() {

	FB.init({
		appId : '337031986416801', // App ID fbtest = 624790460881207 actuarize = 337031986416801
		channelUrl : '//www.actuarize.appspot.com/scripts/channel.html', // Channel File
		status : false, // check login status
		cookie : true, // enable cookies to allow the server to access the session
		xfbml : true // parse XFBML
	});

	// Additional init code here
	FB.getLoginStatus(function(response) {
		console.log(response.status);
		if (response.status === 'connected') {
			// connected
			//testAPI();
		} else if (response.status === 'not_authorized') {
			// not_authorized (here is where I should probably add some onclick events? Instead of Automatic...)
			//console.log('not authorized');
		} else {
			// not_logged_in
			//console.log('not logged in!');
		}
	});

};

$(function() {

	$("button").button();

	// $("button").click(function() {
	// renderStatusBox(action1);
	// return false
	// });

});

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
