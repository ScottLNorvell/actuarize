function onDataReceived(series) {
	var data = [];

	data.push(series);

	// and plot all we got
	$.plot(placeholder, data, options);
};

$(function() {
	var options = {
		lines : {
			show : true
		},
		points : {
			show : true
		},
		xaxis : {
			tickDecimals : 0
		},
		yaxis : {
			max : 100,
			ticks : [0, [20, '20%'], [40, '40%'], [60, '60%'], [80, '80%'], [100, '100%']]
		},
		grid: {
				hoverable: true,
				clickable: true
			},
		legend : {
			show : false
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
			tickDecimals : 0
		},
		yaxis : {
			max : 100,
			ticks : [0, [20, '20%'], [40, '40%'], [60, '60%'], [80, '80%'], [100, '100%']]
		},
		grid: {
				hoverable: true,
				clickable: true
			},
		legend : {
			show : false
		}
	};
	var data = [];
	var data2 = [];
	var placeholder = $("#placeholder");
	var placeholder2 = $("#placeholder2");

	$.plot(placeholder, data, options);
	$.plot(placeholder2, data2, options2);

	var probany = $("span.probany");
	var dataurl = probany.attr('href');
	$.ajax({
		url : dataurl,
		method : 'GET',
		dataType : 'json',
		success : function(series) {

			data.push(series);

			$.plot(placeholder, data, options);
		}
	});
	var proball = $("span.proball");
	var dataurl2 = proball.attr('href');
	$.ajax({
		url : dataurl2,
		method : 'GET',
		dataType : 'json',
		success : function(series) {

			data2.push(series);

			$.plot(placeholder2, data2, options2);
		}
	});
	function showTooltip(x, y, contents) {
		$("<div id='tooltip'>" + contents + "</div>").css({
			position : "absolute",
			display : "none",
			color : '#132D63',
			top : y + 20,
			left : x + 20,
			border : "1px solid #132D63",
			padding : "3px",
			"background-color" : "#BBC8E6",
			"border-radius" : '10px',
			"font-family" : "helvetica",
			opacity : 0.80
		}).appendTo("body").fadeIn(200);
	}
	var previousPoint = null;
	$("#placeholder").bind("plothover", function(event, pos, item) {

		if (item) {
			if (previousPoint != item.dataIndex) {

				previousPoint = item.dataIndex;

				$("#tooltip").remove();
				var x = item.datapoint[0].toFixed(2), y = item.datapoint[1].toFixed(2);

				showTooltip(item.pageX, item.pageY, item.series.label + " in " + Math.floor(x) + " years: " + y + " %");
			}
		} else {
			$("#tooltip").remove();
			previousPoint = null;
		}
	});
	
	$("#placeholder2").bind("plothover", function(event, pos, item) {

		if (item) {
			if (previousPoint != item.dataIndex) {

				previousPoint = item.dataIndex;

				$("#tooltip").remove();
				var x = item.datapoint[0].toFixed(2), y = item.datapoint[1].toFixed(2);

				showTooltip(item.pageX, item.pageY, item.series.label + " in " + Math.floor(x) + " years: " + y + " %");
			}
		} else {
			$("#tooltip").remove();
			previousPoint = null;
		}
	});

});
