from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login

def home(requst):
    return render_to_response('home.html')

   
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                # TODO: Check which page we should redirect to
                return HttpResponseRedirect('/instructions/')
            else:
                # Return a 'disabled account' error message
                return HttpResponseRedirect('/')
        else:
            # Return an 'invalid login' error message.
            return HttpResponseRedirect('/')
    else:
        # TODO: Was a get request. Error?
        return HttpResponseRedirect('/')

  
@login_required()  
def instructions(request):
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