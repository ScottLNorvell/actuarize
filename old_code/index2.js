$(function() {
	$( "#tabs" ).tabs({
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
		
		social_tools: false
	});
	
	$(document).ready(function() {
		$("#tabs").tabs("option", "active", 0);

	});

	

});

