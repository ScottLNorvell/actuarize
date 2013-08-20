$(document).ready(function() {

	// Make vars for the movie parameter inputs:
	var movieName = $('#movieName');
	var movieYear = $('#movieYear'); //hidden and rendered by js
	var movieId = $('#movieId'); 

	// Defining a placeholder text:
	movieName.defaultText('Type a Move Title');

	// Using jQuery UI's autocomplete widget:
	var cache = {}; // we'll cache the results so It doesn't take as long...
	movieName.autocomplete({
		minLength : 3, 
		// pulls data from /tmd-api which gets sexy json results from TMDB
		source : function(request, response) {
			var term = request.term;
			if ( term in cache) {
				response(cache[term]);
				return;
			}

			$.getJSON("/tmdb-api", request, function(data, status, xhr) {
				cache[term] = data;
				response(data);
			});
		},
		// Adds values to appopriate fields for submissionpurposes...
		select : function(event, ui) {
			movieName.val(ui.item.value);
			movieYear.val(ui.item.year);
			movieId.val(ui.item.movie_id);
		}
	});
	
	// turns the button into a pretty jquery ui button
	$('#holder .button').button();
	
	// If valid data, runs renderStatusBox which as a lightbox function that animates while the page loads...
	$('#holder .button').click(function() {
		if (movieName.val().length && movieName.data('defaultText') != movieName.val()) {
			renderStatusBox(action1);
			return false

		}
		return false
	});
	
	// action to be performed by renderStatusBox
	function action1() {
		$('#holder form').submit()
	}

	function renderStatusBox(action) {
		
		// static page with html for status box
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
				
			}
		});

	}

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
			return

		}

		// grabs progress bar and label
		

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
	}

});

$.fn.defaultText = function(value) {

	var element = this.eq(0);
	element.data('defaultText', value);

	element.focus(function() {
		if (element.val() == value) {
			element.val('').removeClass('defaultText');
		}
	}).blur(function() {
		if (element.val() == '' || element.val() == value) {
			element.addClass('defaultText').val(value);
		}
	});

	return element.blur();
}