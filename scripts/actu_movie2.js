$(document).ready(function() {

	// Caching the movieName textbox:
	var movieName = $('#movieName');

	// Defining a placeholder text:
	movieName.defaultText('Type a Move Title');

	// Using jQuery UI's autocomplete widget:
	var cache = {};
	movieName.autocomplete({
		minLength : 3,
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
		}
	});

	$('#holder .button').button();

	$('#holder .button').click(function() {
		if (movieName.val().length && movieName.data('defaultText') != movieName.val()) {
			$('#holder form').submit();
		}
	});
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