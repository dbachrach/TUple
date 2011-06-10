
$(document).ready(function() {
	
	// Set up hover cursor for the two tables
	$('.problem_number_row, .grade_row').hover(function() {
			$(this).css('cursor','pointer');
		}, function() {
			$(this).css('cursor','auto');
	});
	
	// Grade clicks
	$('.grade_row').click(function() {
		student_info = $(this).attr('student_info');
		window.location = "/admin/students/" + student_info + "/";
		return false;
	});
	
	// Question distribution clicks
	$('.problem_number_row').click(function() {
		apprise_info = $(this).attr('apprise_info');
		apprise(apprise_info);
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
    
    var grades_table = $('#grades_table').dataTable( {
        "bAutoWidth": false,
        "bJQueryUI": true,
        "bStateSave": true,
        "sScrollY": "325px",
        "bPaginate": false,
        "bLengthChange": false,
        "bScrollCollapse": true,
        "sDom": '<"H"Tf>t',
		"oLanguage": {
			"sEmptyTable": "No students."
		}
    });

    TableToolsInit.sTitle = "Distribution";
        
    var distribution_table = $('#distribution_table').dataTable( {
        "bAutoWidth": false,
        "bJQueryUI": true,
        "bStateSave": true,
        //"sScrollY": "316px",
        "bPaginate": false,
        "bLengthChange": false,
        //"bScrollCollapse": true,
        "sDom": '<"H"Tf>t',
		"oLanguage": {
			"sEmptyTable": "No problem."
		}
    });
    
    $.fn.dataTableExt.afnFiltering.push(
        function( oSettings, aData, iDataIndex ) {
            var iMin = $('#range-low').html();
            var iMax = $('#range-high').html();
            var grade = aData[2]*1;
            if ( iMin == "" && iMax == "" )
            {
                return true;
            }
            else if ( iMin == "" && grade <= iMax )
            {
                return true;
            }
            else if ( iMin <= grade && "" == iMax )
            {
                return true;
            }
            else if ( iMin <= grade && grade <= iMax )
            {
                return true;
            }
            return false;
        }
    );
    
    
    
    
    $("#grades_graph").bind("plotclick", function (event, pos, item) {
        // secondary axis coordinates if present are in pos.x2, pos.y2,
        // if you need global screen coordinates, they are pos.pageX, pos.pageY
        
        if (item) {
            plot.unhighlight();
            plot.highlight(item.series, item.datapoint);
            $('#range-low').html(item.datapoint[0]);
            $('#range-high').html(item.datapoint[0]);
            grades_table.fnDraw();
        }
    });
        
    $("#grades_graph").bind("plotselected", function (event, ranges) {
        x = Math.round(ranges.xaxis.from);
        y = Math.round(ranges.xaxis.to);
        
        plot.unhighlight();
        i = x;
        while (i <= y) {
            plot.highlight(0, i);
            i++;
        }
        $('#range-low').html(x);
        $('#range-high').html(y);
        grades_table.fnDraw();
    });

    $("#grades_graph").bind("plotunselected", function (event) {
        plot.unhighlight();
        $('#range-low').html("");
        $('#range-high').html("");
        grades_table.fnDraw();
    });	

	$('#grades_table td:first-child').attr('class', $('#grades_table td:first-child').attr('class') + ' left_td');
	$('#distribution_table td:first-child').attr('class', $('#distribution_table td:first-child').attr('class') + ' left_td');
});

function make_plot(data, problem_count) {
    var plot = $.plot($("#grades_graph"), [
        { 
            label: "",  
            data: data, 
            bars: { 
                show: true, 
                fill: true,
                lineWidth: 3,
                align: "center",
            },
            color: "rgb(91,144,151)",
        }
        ], {
            xaxis: {
                ticks: problem_count,
                tickSize: 1,
                tickDecimals: 0,
                min: -.5,
                max: problem_count + 0.5,
            },
            yaxis: {
                min: 0,
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
            },
            selection: { 
                mode: "x" ,
            }
    });
}