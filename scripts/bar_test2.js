//Working version of Status Lightbox for standalone page...

$(function() {
	
	function progHappens() {
		var progressbar = $("#progressbar"), progressLabel = $(".progress-label");
		var pos = 0;
		var waitProg = 10;
		var waitLabel = 2000;
		var messages = ['Complete!', 'Wait, why is this still going on?', "I can't deal with this", "Complete!", "Where's my Page?","This stopped being funny..."];
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

		setTimeout(progress, 500);
		//console.log('progress timeout set')
	}

	// This code to happen on doc reload
	$("button.fadein").click(function() {
		$('#lightbox').fadeIn(500);
		$("#lightbox-panel").fadeIn({
			duration : 500,
			complete : progHappens
		});
	});

	$('button.fadeout').click(function() {
		$("#lightbox").fadeOut(300);
		$('#lightbox-panel').fadeOut({
			duration : 300,
			easing : 'easeOutBounce',
			complete : function() {
				document.location.reload(true)
			}
		})
	});

});

