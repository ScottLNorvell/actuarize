$(function() {
	$("#tabs").tabs({
		collapsible : true,
		active : false,
		show : {
			effect : "blind",
			easing : "easeInOutExpo",
			duration : 400
		},
		hide : {
			effect : "blind",
			easing : "easeInOutExpo",
			duration : 250
		}
	});

	$(".button").button();

	$("a[rel^='prettyPhoto']").prettyPhoto({
		animation_speed : 'normal',
		theme : 'dark_rounded',
		callback : function() {
			window.location.hash = '';
			history.pushState('', document.title, window.location.pathname);
		},

		social_tools : false
	});

	$(document).ready(function() {
		$("#tabs").tabs("option", "active", 0);

	});

	var fbButton = $("#facebook a")
	fbButton.click(function(e) {
		e.preventDefault
		console.log('i just clicked the button...')
		renderStatusBox(action1);
		return false
	});

	function action1() {
		var href = fbButton.attr('href')
		//alert("I'm in the action now with the href of " + href)		
		window.location = href
	}

	function renderStatusBox(action) {
		console.log("I'm in the Function Render Status Box!");
		//console.log(action)
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
		return false
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
	}

});

