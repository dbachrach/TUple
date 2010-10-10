from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


  
@login_required()  
def instructions(request):
	# TODO: Check if the user has already started exam. If so, redirect to /exam/
    return render_to_response("instructions.html")


@login_required()
def start(request):
    if request.method == 'POST':
        return HttpResponseRedirect('/exam/')
    else:
        return HttpResponseRedirect('/')

@login_required()    
def exam(request):
    return HttpResponse("Exam")


@login_required()    
def finished(request):
    # TODO: Should we logout? logout(request)
    return render_to_response('finished.html')


def closed(request):
    return render_to_response('closed.html')