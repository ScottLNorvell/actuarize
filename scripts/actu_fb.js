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

	$("#gallery a img").tooltip();

	$("#gallery a[rel^='prettyPhoto']").prettyPhoto({
		animation_speed : 'normal',
		theme : 'dark_rounded',
		slideshow : 10000,
		autoplay_slideshow : true,
		overlay_gallery : false,
		social_tools : false,
		callback : function() {
			window.location.hash = '';
			history.pushState('', document.title, window.location.pathname);
		}
	});
	var sliderapi = $('span.probs').attr('href');
	$("#slider").slider({
		range : "min",
		value : 10,
		min : 1,
		max : 100,
		slide : function(event, ui) {
			$("#amount").val(ui.value);
		},
		stop : function(event, ui) {
			$.ajax({
				url : sliderapi + ui.value,
				method : 'GET',
				dataType : 'json',
				success : function(probs) {
					

					console.log(probs);
					console.log(probs.probany);
					$("#results-window").remove();
					$('<div id="results-window"><p>Probability of someone dying: ' + probs.probany + '</p>' + '<p>Probability of everyone dying: ' + probs.proball + '</p></div>').css({
						display : "none"
					}).appendTo('#slider-results').fadeIn(500);
				}
			});
		}
	});
	$("#amount").val($("#slider").slider("value"));

	$(document).ready(function() {
		$("#tabs").tabs("option", "active", 0);

	});

	$(".button").button();

});

