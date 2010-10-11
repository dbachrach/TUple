from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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
def instructions(request, popup=False):
    # TODO: Check if the user has already started exam. If so, redirect to /exam/
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
        
        
        
