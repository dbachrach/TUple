$(document).ready(function() {
	var current = new Date();
	var month = current.getMonth() + 1;
	var day = current.getDate();
	var year = current.getFullYear();
	var date_str = month + "/" + day + "/" + year;
	$('#id_date').attr('value', date_str);
});