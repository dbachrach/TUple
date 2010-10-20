from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from exam_settings import EXAM_SETTINGS
from django.template import RequestContext
from TUple.exam.models import Problem, ExamGroup

# TODO: Handle retakes
def check_closed(f):
    def _inner(*args, **kwargs):
        if EXAM_SETTINGS['exam_closed']
            return closed(*args, **kwargs)
        else:
            return f(*args, **kwargs)
    return _inner


@check_closed
@login_required
def didlogin(request):
    if request.user.is_staff:
        return HttpResponseRedirect('/admin/')
    elif request.user.get_user_profile().is_in_progress():
        return HttpResponseRedirect('/exam/')
    elif request.user.get_user_profile().has_finished():
        return HttpResponseRedirect('/') # TODO: Append a message, saying they have already finished the exam
    else:
        return HttpResponseRedirect('/instructions/')
    
    
@check_closed
@login_required
def instructions(request, popup=False):
    return render_to_response("instructions.html", {'popup' : popup}, context_instance=RequestContext(request))



@check_closed
@login_required
def start(request):
    request.user.get_user_profile().start_exam()
    
    if request.method == 'POST':
        return HttpResponseRedirect('/exam/')
    else:
        return HttpResponseRedirect('/')


@check_closed
@login_required    
def exam(request):
    if !request.user.get_user_profile().is_in_progress():
        return HttpResponseRedirect('/')
        
    return render_to_response("exam.html", {'problems' : Problem.objects.all()}, context_instance=RequestContext(request))



@check_closed
@login_required
def end(request):
    request.user.get_user_profile().end_exam()
    
    if request.method == 'POST':
        return HttpResponseRedirect('/finished/')
    else:
        return HttpResponseRedirect('/')


@check_closed
@login_required  
def finished(request):
    return render_to_response('finished.html', context_instance=RequestContext(request))


def closed(request):
    return render_to_response('closed.html', context_instance=RequestContext(request))



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
        
    # TODO: Make sure user is authorized to access problem with id=problem_id

    if request.method == 'POST':
        return post_problem(request, problem)
    elif request.method == 'GET':
        return get_problem(request, problem)
    else:
        # TODO: Error?
        return HttpResponse("error")



@check_closed
@login_required 
def get_problem(request, problem):  
    return render_to_response("problem.html", {'problem' : problem}, context_instance=RequestContext(request))



@check_closed
@login_required 
def post_problem(request, problem):
    if 'answer' in request.POST and request.POST['answer']:
        answer_id = request.POST['answer']
        answer = Answer.objects.get(id=answer_id) 
        # TODO: Handle exceptions
        
        # TODO: Do any validation on answer
        if problem != answer.problem:
            # TODO: Error
            return HttpResponse("Error: problem != answer.problem")
            
        # Save answer to user's answer sheet
        request.user.get_user_profile().answer_problem(problem, answer)
    return HttpResponse('')
        
        


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin(request, group_name=None):
    if group_name is None:
        try:
            exam_group = ExamGroup.objects.get(active=True)
        except ExamGroup.DoesNotExist:
            # TODO: Return error
            return HttpResponse("error: no active group exists")
        except ExamGroup.MultipleObjectsReturned:
            # TODO: Return error
            return HttpResponse("error: multiple active groups exist")
    else:
        try:
            exam_group = ExamGroup.objects.get(name=group_name)
        except ExamGroup.DoesNotExist:
            # TODO: Return error
            return HttpResponse("error: no group with name " + group_name)
        except ExamGroup.MultipleObjectsReturned:
            # TODO: Return error
            return HttpResponse("error: multiple groups with naame " + group_name)
          
    stats = exam_group.calculate_statistics()
    return render_to_response("admin.html", {'stats' : stats, 'problems' : exam_group.problems.all()}, context_instance=RequestContext(request))
