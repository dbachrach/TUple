from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from TUple.exam.models import Problem


site_settings = {'exam_name' : settings.EXAM_NAME}

def check_closed(f):
    def _inner(*args, **kwargs):
        if settings.EXAM_CLOSED:
            return closed(*args, **kwargs)
        else:
            return f(*args, **kwargs)
    return _inner


@check_closed
@login_required
def didlogin(request):
    # TODO: Check if the user has already started exam. If so, redirect to /exam/
    if (request.user.is_staff):
        return HttpResponseRedirect('/admin/')
    # elif user has already started exam:
        #return HttpResponseRedirect('/exam/')
    else:
        return HttpResponseRedirect('/instructions/')
    
    
@check_closed
@login_required
def instructions(request, popup=False):
    return render_to_response("instructions.html", {'popup' : popup})



@check_closed
@login_required
def start(request):
    # TODO: Do actions required at start
    if request.method == 'POST':
        return HttpResponseRedirect('/exam/')
    else:
        return HttpResponseRedirect('/')


@check_closed
@login_required    
def exam(request):
    return render_to_response("exam.html", {'problems' : Problem.objects.all(), 'answer_choices' : ('a', 'b', 'c', 'd', 'e',)})



@check_closed
@login_required
def end(request):
    # TODO: Do actions required at end
    if request.method == 'POST':
        return HttpResponseRedirect('/finished/')
    else:
        return HttpResponseRedirect('/')

@check_closed
@login_required  
def finished(request):
    # TODO: Should we logout? logout(request)
    return render_to_response('finished.html')


def closed(request):
    return render_to_response('closed.html')



@check_closed
@login_required
def problem(request, problem_id):
    try:
        problem = Problem.objects.get(id=problem_id)
    except Problem.DoesNotExist:
        # TODO: Return error
        return HttpResponse("error")
    except Problem.MultipleObjectsReturned:
        # TODO: Return error
        return HttpResponse("error")

    if request.method == 'POST':
        return post_problem(request, problem)
    elif request.method == 'GET':
        return get_problem(request, problem)
    else:
        # TODO: Error?
        return HttpResponse("")



@check_closed
@login_required 
def get_problem(request, problem):  
    return render_to_response("problem.html", {'problem' : problem})



@check_closed
@login_required 
def post_problem(request, problem):
    if 'answer' in request.POST and request.POST['answer']:
        answer = request.POST['answer']
        # TODO: Do any validation on answer
        # TODO: Save answer to user's choices
    return HttpResponse('')
        
        


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin(request, year=2010):
    # TODO: Set year to be current year by default
    # TODO: Check for invalid year   
    stats = calculate_statistics()
    return render_to_response("admin.html", {'stats' : stats, 'problems' : Problem.objects.all()})


def calculate_statistics():
	question_count = 30
	finished_students_count = 5
	total_students_count = 24
	finished_students_percentage = float(finished_students_count) / float(total_students_count) * 100
	average_score = 13
	average_score_percentage = float(average_score) / float(question_count) * 100
	standard_deviation = 12.2
	high_score = 29
	high_score_percentage = float(high_score) / float(question_count) * 100
	low_score = 8
	low_score_percentage = float(low_score) / float(question_count) * 100
	return locals()
	
	