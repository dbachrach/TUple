$(document).ready(function() {
	
	// Set up hover cursor for the two tables
	$('.stat_row').hover(function() {
			stat_num = $(this).attr('stat_num');
			$(this).css('cursor','pointer');
			plotAccordingToChoices(stat_num);
		}, function() {
			$(this).css('cursor','auto');
			plotAccordingToChoices(null);
	});
	
	// Session clicks
	$('.stat_row').click(function() {
		stat_info = $(this).attr('stat_info');
		window.location = "/admin/sessions/" + stat_info + "/";
		return false;
	});
	
    TableToolsInit.oFeatures.bXls = false;
    TableToolsInit.oFeatures.bCopy = false;
    TableToolsInit.oFeatures.bPrint = false;
    TableToolsInit.oBom.bXls = false;
    TableToolsInit.iButtonHeight = 24;
    TableToolsInit.iButtonWidth = 24;
    TableToolsInit.sSwfPath = "/media/js/tabletools/swf/ZeroClipboard.swf";
    TableToolsInit.sTitle = "Grades";
    
    var grades_table = $('#stats_table').dataTable( {
        "bAutoWidth": false,
        "bJQueryUI": true,
        "bStateSave": true,
        // "sScrollY": "325px",
        "bPaginate": false,
        "bLengthChange": false,
        // "bScrollCollapse": true,
        "sDom": '<"H"Tf>t',
    });

	var datasets = [
		{% for session in sessions %}
	        { 
	            label: "{{ session.name }}",  
	            data: eval('{{ session.grade_distribution }}'), 
	            lines: { 
	                show: true, 
	                fill: true,
	                lineWidth: 3,
	                align: "center",
	            },
	            color: "rgb(91,144,151)",
	        },
		{% endfor %}
        ];
	
	// hard-code color indices to prevent them from shifting as
    // countries are turned on/off
    var i = 0;
    $.each(datasets, function(key, val) {
        val.color = i;
        i++;
    });

	
	var max_y_value = -1;
	
	for (var i = 0; i < datasets.length; i++) {
		var set = datasets[i];
		d = set['data'];
		for (var j = 0; j < d.length; j++) {
			var el = d[j];
			var val = el[1];
			if (max_y_value < val) {
				max_y_value = val;
			}
		}
	}

	function plotAccordingToChoices(plot_choice) {
        var data = [];

		if (plot_choice == null) {
			data = datasets;
		}
		else {
			data.push(datasets[plot_choice])
		}

        if (data.length > 0) {
            $.plot($("#grades_graph"), data, {
				xaxis: {
	                ticks: {{ problem_count }},
	                tickSize: 1,
	                tickDecimals: 0,
	                min: -.5,
	                max: {{ problem_count }} + 0.5,
	            },
	            yaxis: {
	                min: 0,
					max: max_y_value + 0.5,
	                tickSize: 1,
	                tickDecimals: 0,
	            },
	            grid: {
	                backgroundColor: { colors: ["#fff", "#eee"] },
	                hoverable: true, 
	                clickable: true,
	                borderWidth: 1,
	                borderColor: "#C1DAD7",
	                verticalLinesX1: false,
	            }
            });
		}
    }

	plotAccordingToChoices(null);
});