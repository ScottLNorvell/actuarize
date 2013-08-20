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

	$("#gallery a[rel^='prettyPhoto']").prettyPhoto({
		animation_speed : 'normal',
		theme : 'dark_rounded',
		slideshow : 10000,
		autoplay_slideshow : true,
		social_tools : false,
		callback : function() {
			window.location.hash = '';
			history.pushState('', document.title, window.location.pathname);
		}
	});

	$(document).ready(function() {
		$("#tabs").tabs("option", "active", 0);

	});

	$(".button").button();

});

