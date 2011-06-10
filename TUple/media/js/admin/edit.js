$(document).ready(function() {
	
	TableToolsInit.oFeatures.bXls = false;
    TableToolsInit.oFeatures.bCopy = false;
    TableToolsInit.oFeatures.bPrint = false;
	TableToolsInit.oFeatures.bCsv = false;
    TableToolsInit.oBom.bXls = false;
    TableToolsInit.iButtonHeight = 24;
    TableToolsInit.iButtonWidth = 24;
    TableToolsInit.sSwfPath = "/media/js/tabletools/swf/ZeroClipboard.swf";
    TableToolsInit.sTitle = "Students";
    
    var grades_table = $('#students_table').dataTable( {
        "bAutoWidth": false,
        "bJQueryUI": true,
        "bStateSave": true,
        "sScrollY": "325px",
        "bPaginate": false,
        "bLengthChange": false,
        "bScrollCollapse": true,
        "sDom": '<"H"T<"toolbar">>t',
		"oLanguage": {
			"sEmptyTable": "No students."
		}
    });

	$('.toolbar').html('<button id="upload_csv">Upload CSV of Students</button> <button id="add_student">Add Student</button>');
	$('.toolbar').attr('style', 'float:right');
	
	$('#add_student').click(function() {
		apprise('<h3>Add Student</h3>\
        <form id="add_student_form" action="/admin/sessions/{{ exam_group.name }}/edit/add_student/" method="post">\
        <div class="input_area">\
        <p><label for="">Last Name:</label> <input type="text" name="last_name"  id="add_student_name" maxlength="100" /></p>\
        <p><label for="">Student ID:</label> <input type="text" name="student_id" id="add_student_id" maxlength="100" /></p>\
        </div>\
        </form>', 
			{'confirm':true, 'textOk':'Add'},
			function(r) {
				if (r) {					
                    $('#add_student_form').submit();
				}
			}
		);
		return false;
	});
	
	
	$('#upload_csv').click(function() {		
		var str = '<h3>Upload CSV of Students</h3>\
			   <form id="upload_form" action="/admin/sessions/{{ exam_group.name }}/edit/csv/" method="post" enctype="multipart/form-data">\
			   <div class="input_area" id="upload_form">\
				<p><label for="">File:</label> <input id="" type="file" id="file" name="file" /></p>\
			   </div>\
			   <form>';

		apprise(str, {'confirm':true, 'textOk':'Upload'},
			function(r) {
				if (r) {
					$('#upload_form').submit();
				}
			}
		);
		
		return false;
	});
	
	$('#students_table td:first-child').attr('class', $('#students_table td:first-child').attr('class') + ' left_td');
});