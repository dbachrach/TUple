
var oldQuestionNum = 0;
var questionNum = 1;
var question_count = 0;
var hr = 0;
var min = 0;
var sec = 0;

function startTest(num_questions, time_left) {
	questionNum = 1;
	question_count = num_questions
	
	hr = parseInt(time_left / 3600);
	min = parseInt((time_left % 3600) / 60);
	sec = parseInt((time_left % 3600) % 60);
	
	changeQuestion();
	updateTimer(); 
}

function bindArrowShortcuts() {
    $(document).bind('keydown', {keys: 'left'}, function (evt) {
	    prevQuestion();
	    return false;
	});
	$(document).bind('keydown', {keys: 'right'}, function (evt) {
	    nextQuestion();
	    return false;
	});
}

function changeQuestion() {

	// Load the new question
	$.get('/problem/' + questionNum + '/', function(data) {
		$('#question').html(data);
		//MathJax.Hub.Queue(["Typeset",MathJax.Hub,"question"]);
	});
	
	// Binds shortcut keys for each of the answers to this problem
	$(document).unbind('keydown');
	bindArrowShortcuts();
	$.getJSON('/hotkeys/' + questionNum + '/', function(data) {
	    problem_id = data['problem_id']
	    
	    var answers = data['answers'];
	    for (var answer_id in answers) {
	        var letter = answers[answer_id];
	        $(document).bind('keydown', {keys: letter, answer: answer_id},  function (evt) {
        	    answerSelected(problem_id, evt.data.answer);
        	    return false;
        	});
	    }
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
		var i = '#answer_form_row_' + oldQuestionNum;
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
	$('#answer_form_row_' + questionNum).css({
		color: '#FFFFFF',
		background: '#ffea96',
		fontWeight: 'bold'
	}, "fast");
	
	// Disable the previous row radio buttons
	var old_row_inputs = $('#answer_form_row_' + oldQuestionNum + " :radio");
 	if (oldQuestionNum != 0) {
		old_row_inputs.attr('disabled', true);
	}
	
	// Enable the current row radio buttons
	var current_row_inputs = $('#answer_form_row_' + questionNum + " :radio");
	current_row_inputs.attr('disabled', false);
	
	// Scroll the question to the top
	$('#answer_scroller').scrollTop = $('row_'+questionNum+'_link').scrollHeight * ( ((questionNum / 5) | 0) * 5);
}

function prevQuestion() {
	if (questionNum > 1) {
		oldQuestionNum = questionNum;
		questionNum--;
		changeQuestion();
	}
}

function nextQuestion() {
	if (questionNum < question_count) {
		oldQuestionNum = questionNum;
		questionNum++;
		changeQuestion();
	}
}

function selectQuestion(q) {
	if (q >= 1 && q <= question_count) {
		oldQuestionNum = questionNum;
		questionNum = q;
		changeQuestion();
	}
}

function updateTimer() {
	sec = sec - 1;
	if (sec == -1) {
		sec = 59;
		min = min - 1;
		if(min == -1) {
		    min = 59;
		    hr = hr - 1;
		    if (hr == -1) {
		        timer_done();
		    }
		}
	}
	var hr_d = "";
	if (hr > 0) {
	    hr_d = hr + ":";
	}
	var min_d = min;
	if (min < 10) {
		min_d = "0" + min;
	}
	var sec_d = sec;
	if (sec < 10) {
		sec_d = "0" + sec;
	}
	
	$('#timer_string').html(hr_d + min_d + ":" + sec_d);
	setTimeout("updateTimer()",1000);
}

function timer_done() {
	$('#answer_key_form').submit();
}

function answerSelected(question_id, answer_id) {
    // Right now question_id is not used. We assume that the question_id is questionNum since a user can only answer the current question.
    
	// Select the appropriate radio button
	$('#answer_form_problem_' + questionNum + '_answer_' + answer_id).attr('checked', true);
	$('#problem_' + questionNum + '_answer_' + answer_id).attr('checked', true);
	
	// Send an AJAX request to save the answer
	$.post('/problem/' + questionNum + '/', {answer: answer_id});
}

function checkFinished() {
	for(var x = 1; x <= question_count; x++) {
		var radio_buttons = $('#answer_form_row_' + x + " :radio");
		
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


$(document).ready(function() {
	
	$("#finish_test_button").click(function() {
	    return checkFinished();
	});
	
	$("#help_link a").click(function() {
		window.open('/popup/instructions/','Instructions','width=830,height=580,scrollbars=1');
		return false;
	});
	
	$("#prev_link").click(function() {
		prevQuestion();
		return false;
	});
	
	$("#next_link").click(function() {
		nextQuestion();
		return false;
	});
	
	$("#periodic_table").click(function() {
		window.open('{{ media_url }}images/ptable.gif','Periodic Table','width=806,height=580');
		return false;
	});
	
	$(function() {
        $('.rollover').hover(function() {
            var currentImg = $('img', this).attr('src');
            $('img', this).attr('src', $('img', this).attr('hover'));
            $('img', this).attr('hover', currentImg);
        }, function() {
            var currentImg = $('img', this).attr('src');
            $('img', this).attr('src', $('img', this).attr('hover'));
            $('img', this).attr('hover', currentImg);
        });
    });

   	startTest({{ problem_data|length }}, {{ time_left }});
});
