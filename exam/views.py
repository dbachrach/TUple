from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from TUple.exam.models import Problem


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
def finished(request):
    # TODO: Should we logout? logout(request)
    return render_to_response('finished.html')


def closed(request):
    return render_to_response('closed.html')