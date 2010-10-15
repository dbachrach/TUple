
var oldQuestionNum = 0;
var questionNum = 1;
var question_count = 0;

function startTest(num_questions) {
	questionNum = 1;
	question_count = num_questions
	changeQuestion();
	updateTimer();
	initializeKeyboardShortcuts();    
}

function initializeKeyboardShortcuts() {
    $(document).bind('keydown', 'left', function (evt) {
	    prevQuestion();
	    return false;
	});
	$(document).bind('keydown', 'right', function (evt) {
	    nextQuestion();
	    return false;
	});
	$(document).bind('keydown', 'a', function (evt) {
	    answerSelected(questionNum, 'A');
	    return false;
	});
	$(document).bind('keydown', 'b', function (evt) {
	    answerSelected(questionNum, 'B');
	    return false;
	});
	$(document).bind('keydown', 'c', function (evt) {
	    answerSelected(questionNum, 'C');
	    return false;
	});
	$(document).bind('keydown', 'd', function (evt) {
	    answerSelected(questionNum, 'D');
	    return false;
	});
	$(document).bind('keydown', 'e', function (evt) {
	    answerSelected(questionNum, 'E');
	    return false;
	});
}

function changeQuestion() {

	// Load the new question
	$.get('/problem/' + questionNum + '/', function(data) {
        // if (oldQuestionNum < questionNum) {
        //     $('#question-left').html(data);
        //             // $('#question-right').fadeIn('fast');
        //             // $('#question-left').fadeOut('fast');
        // }
        // else if (oldQuestionNum > questionNum) {
        //     $('#question-left').html(data);
        //             // $('#question-left').fadeIn('fast');
        //             // $('#question-right').fadeOut('fast');
        // }
        // else {
        //     $('#question-center').html(data);
        // }
		$('#question').html(data);
	});
	
    
	// Show or hide the previous/next question links
	if (questionNum == 1 && questionNum == question_count) {
		$('#prev_link').fadeOut("fast");
		$('#next_link').fadeOut("fast");
		$('#pipe_symbol').fadeOut("fast");
	}
	else if (questionNum == 1) {
	    $('#pipe_symbol').fadeOut("fast");
		$('#prev_link').fadeOut("fast", function() {
		   	$('#next_link').fadeIn("fast");
		});
	}
	else if (questionNum == question_count) {
	    $('#pipe_symbol').fadeOut("fast");
		$('#next_link').fadeOut("fast", function() {
		    $('#prev_link').fadeIn("fast");
		});
	}
	else {
		$('#prev_link').fadeIn("fast");
		$('#next_link').fadeIn("fast");
		$('#pipe_symbol').fadeIn("fast");
	}

	
	// Reset the previous row to its unselected state
	if (oldQuestionNum != 0) { 
		var i = '#answerFormRow' + oldQuestionNum;
		if(oldQuestionNum % 2 == 0) {
			$(i).css({
				color: '#4f6b72',
				background: '#E5E5E5',
				fontWeight: 'normal'
			}, "fast");
		}
		else {
			$(i).css({
				color: '#4f6b72',
				background: '#fff',
				fontWeight: 'normal'
			}, "fast");
		}
	}
	
	// Set the current row to its selected state
	$('#answerFormRow' + questionNum).css({
		color: '#FFFFFF',
		background: '#ffea96',
		fontWeight: 'bold'
	}, "fast");
	
	// Disable the previous row radio buttons
	var old_row_inputs = $('#answerFormRow' + oldQuestionNum + " :radio");
 	if (oldQuestionNum != 0) {
		old_row_inputs.attr('disabled', true);
	}
	
	// Enable the current row radio buttons
	var current_row_inputs = $('#answerFormRow' + questionNum + " :radio");
	current_row_inputs.attr('disabled', false);
	
	// Scroll the question to the top
	$('#answerScroller').scrollTop = $('row_'+questionNum+'_link').scrollHeight * ( ((questionNum / 5) | 0) * 5);
}

function prevQuestion() {
	if(questionNum > 1) {
		oldQuestionNum = questionNum;
		questionNum--;
		changeQuestion();
	}
}

function nextQuestion() {
	if(questionNum < question_count) {
		oldQuestionNum = questionNum;
		questionNum++;
		changeQuestion();
	}
}

function selectQuestion(q) {
	if(q >= 1 && q <= question_count) {
		oldQuestionNum = questionNum;
		questionNum = q;
		changeQuestion();
	}
}


var min = 60; // TODO: Set min and sec based on time from django
var sec = 0;
function updateTimer() {

	sec = sec - 1;
	if(sec == -1) {
		sec = 59;
		min = min - 1;
		if(min==-1) {
			timer_done();
		}
	}
	var min_d = min;
	if(min< 10) {
		min_d = "0" + min;
	}
	var sec_d = sec;
	if(sec<10) {
		sec_d = "0" + sec;
	}
	
	$('#timer_string').html(min_d + ":" + sec_d);
	setTimeout("updateTimer()",1000);
}

function timer_done() {
	$('#answerKeyForm').submit();
}

function answerSelected(question_id, answer_value) {
	// Select the appropriate radio button in the table
	$('#row' + question_id + '-input' + answer_value.toLowerCase()).attr('checked', true);
	
	// Select the appropriate radio button in the problem list
	$('#problem' + question_id + '-input' + answer_value.toLowerCase()).attr('checked', true);
	
	// Send an AJAX request to save the answer
	$.post('/problem/' + question_id + '/', {answer : answer_value});
}

function checkFinished() {
	for(var x = 1; x <= 3000000; x++) {
		var radio_buttons = $('#answerFormRow' + x + " :radio");
		
		var has_selection = false;
		radio_buttons.each(function () {
		    if ($(this).is(':checked')) {
		        has_selection = true;
		    }
		});

		
        if (!has_selection) {
            alert("You have not answered all the questions.");
            return false;
        }
	}

	return confirm("Are you sure you are finished?");
}
