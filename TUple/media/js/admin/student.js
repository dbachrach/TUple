$(document).ready(function() {
	
	// Set up hover cursor for the two tables
	$('.problem_number_row').hover(function() {
			$(this).css('cursor','pointer');
		}, function() {
			$(this).css('cursor','auto');
	});
	
	// Problem clicks
	$('.problem_number_row').click(function() {
		apprise_info = $(this).attr('apprise_info');
		apprise(apprise_info);
		return false;
	});
	
	TableToolsInit.oFeatures.bXls = false;
	TableToolsInit.oFeatures.bCopy = false;
	TableToolsInit.oFeatures.bPrint = false;
	TableToolsInit.oBom.bXls = false;
	TableToolsInit.iButtonHeight = 12;
	TableToolsInit.iButtonWidth = 12;
	TableToolsInit.sSwfPath = "/media/js/tabletools/swf/ZeroClipboard.swf"
	
	var answers_table = $('#answers_table').dataTable( {
		"bAutoWidth": false,
	    "bJQueryUI": true,
	    "bStateSave": true,
        "bPaginate": false,
        "bLengthChange": false,
		"sDom": 't',
	});
});