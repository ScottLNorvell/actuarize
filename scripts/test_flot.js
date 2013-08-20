$(function() {
	var options = {
		lines : {
			show : true
		},
		points : {
			show : true
		},
		xaxis : {
			tickDecimals : 0,
			tickSize : 1
		}
	};
	var options2 = {
		lines : {
			show : true
		},
		points : {
			show : true
		},
		xaxis : {
			tickDecimals : 0,
			tickSize : 1
		}
	};
	var data = [];
	var data2 = [];
	var placeholder = $("#placeholder");
	var placeholder2 = $("#placeholder2");

	$.plot(placeholder, data, options);
	$.plot(placeholder2, data2, options2);

	// fetch one series, adding to what we got
	var alreadyFetched = {};

	$("input.fetchSeries").click(function() {
		var button = $(this);

		// find the URL in the link right next to us
		var dataurl = button.siblings('a').attr('href');

		// then fetch the data with jQuery
		function onDataReceived(series) {

			// let's add it to our current data
			if (!alreadyFetched[series.label]) {
				alreadyFetched[series.label] = true;
				data.push(series);
			}

			// and plot all we got
			$.plot(placeholder, data, options);
		}


		$.ajax({
			url : dataurl,
			method : 'GET',
			dataType : 'json',
			success : onDataReceived
		});
	});
	
	$("input.fetchSeries2").click(function() {
		var button = $(this);

		// find the URL in the link right next to us
		var dataurl = button.siblings('a').attr('href');

		// then fetch the data with jQuery
		function onDataReceived(series) {

			// let's add it to our current data
			if (!alreadyFetched[series.label]) {
				alreadyFetched[series.label] = true;
				data2.push(series);
			}

			// and plot all we got
			$.plot(placeholder2, data2, options2);
		}


		$.ajax({
			url : dataurl,
			method : 'GET',
			dataType : 'json',
			success : onDataReceived
		});
	});
}); 