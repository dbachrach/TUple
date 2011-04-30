from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import views as AuthViews
from django.template import RequestContext
from django.utils import simplejson
from django.contrib import messages
from TUple.exam.models import Problem, ExamGroup, Answer, Exam, ExamForm, UserProfile, ExamGroupForm
from django.views.generic import create_update
from django.views.decorators.cache import cache_page
import csv


def check_closed(f):
    def _inner(*args, **kwargs):
        active_exam_count = len(ExamGroup.objects.filter(active=True))
        request = args[0]
        
        if active_exam_count == 0 and not request.user.get_profile().can_retake():
            return closed(*args, **kwargs)
        else:
            return f(*args, **kwargs)
    return _inner


@check_closed
@login_required
def didlogin(request):
    if request.user.is_staff:
        return HttpResponseRedirect('/admin/')
    if not request.user.get_profile().is_allowed_to_test():
        messages.info(request, 'Login failed. You are not allowed to take this exam currently.')
        return HttpResponseRedirect('/')
    elif request.user.get_profile().is_in_progress():
        return HttpResponseRedirect('/exam/')
    elif request.user.get_profile().has_finished():
        messages.info(request, 'Login failed. You have already completed the test. You may not login again.')
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/instructions/')
    
    
@check_closed
@login_required
def instructions(request, popup=False):
    exam_group = request.user.get_profile().exam_group
    problem_count = exam_group.sorted_problems().count()
    exam_length = exam_group.get_examination_time_string()
    return render_to_response("instructions.html", {'popup': popup, 
                                                    'problem_count': problem_count, 
                                                    'exam_length': exam_length}, 
                                                    context_instance=RequestContext(request))


@check_closed
@login_required
def start(request):
    request.user.get_profile().start_exam()
    
    if request.method == 'POST':
        return HttpResponseRedirect('/exam/')
    else:
        return HttpResponseRedirect('/')


@check_closed
@login_required    
def exam(request):
    if not request.user.get_profile().is_in_progress():
        return HttpResponseRedirect('/')
        
    time_left = request.user.get_profile().time_left()  
    if time_left == -1:
        return HttpResponseRedirect('/finished/')
    
    exam_group = request.user.get_profile().exam_group
    problems = exam_group.sorted_problems()
    
    exam_answers_per_problem = exam_group.answers_per_problem
    
    # Creates a list of each problem's selected answer
    chosen_answers = map(request.user.get_profile().get_answer_for_problem, problems)

    # Combines the problems and their chosen answer into a single list where each element 
    # is a dictionary containting the problem and the selected answer
    problem_data = map(lambda p, c : {'problem': p, 'chosen_answer': c}, problems, chosen_answers)
    
    return render_to_response("exam.html", {'problem_data': problem_data, 
                                            'time_left': time_left, 
                                            'exam_answers_per_problem': exam_answers_per_problem}, 
                                            context_instance=RequestContext(request))


@check_closed
@login_required
def end(request):
    request.user.get_profile().end_exam()
    
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
def hotkeys(request, problem_index):
    problem = request.user.get_profile().get_problem_at_number(problem_index)
    if problem is None:
        return HttpResponse("")
        
    # Generate a JSON response that lists the problem id, and all its answer ids and letters
    answers = {}
    for answer in problem.sorted_answers():
        answers[answer.id] = answer.letter
        
    result = {'problem_id': problem.id, 'answers': answers}
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")


@check_closed
@login_required
def problem(request, problem_index):
    problem = request.user.get_profile().get_problem_at_number(problem_index)
    if problem is None:
        return HttpResponse("Problem not found.")

    if request.method == 'POST':
        return post_problem(request, problem)
    elif request.method == 'GET':
        return get_problem(request, problem)
    else:
        return HttpResponse("Error. Not a POST or GET request.")


@check_closed
@login_required 
def get_problem(request, problem):  
    chosen_answer = request.user.get_profile().get_answer_for_problem(problem)
    return render_to_response("problem.html", {'problem': problem, 
                                               'chosen_answer': chosen_answer}, 
                                               context_instance=RequestContext(request))

    
@check_closed
@login_required 
def post_problem(request, problem):
    if 'answer' in request.POST and request.POST['answer']:
        answer_id = request.POST['answer']
        try:
            answer = Answer.objects.get(id=answer_id) 
        except Answer.DoesNotExist:
            return HttpResponse("Error: No active group exists.")
        except Answer.MultipleObjectsReturned:
            return HttpResponse("Error: Multiple active groups exist.")
        
        # Ensure the user has provided an appropriate answer to the problem.
        if problem != answer.problem:
            return HttpResponse("Error: Incorrect problem.")
            
        # Save answer to user's answer sheet
        request.user.get_profile().answer_problem(problem, answer)
    return HttpResponse('')
        
     
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin(request):     
    return HttpResponseRedirect('/admin/sessions/')
   
    
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_sessions(request):  
    try:
        exam_group = ExamGroup.objects.get(active=True)
    except ExamGroup.DoesNotExist:
        return HttpResponse("Error: No active group exists.")
    except ExamGroup.MultipleObjectsReturned:
        return HttpResponse("Error: multiple active groups exist.")
    return HttpResponseRedirect('/admin/sessions/' + exam_group.name + '/')
            
    
@login_required
@user_passes_test(lambda u: u.is_staff)
@cache_page(60 * 5)
def admin_session(request, group_name):
    if group_name:
        try:
            exam_group = ExamGroup.objects.get(name=group_name)
        except ExamGroup.DoesNotExist:
            return HttpResponse("Error: No group with name " + group_name)
        except ExamGroup.MultipleObjectsReturned:
            return HttpResponse("Error: Multiple groups with name " + group_name)
    else:
        return HttpRespone("Error: No group name provided " + group_name)
    
    return render_to_response("admin_session.html", 
        {
            'stats': exam_group.calculate_statistics(), 
            'problems': exam_group.sorted_problems(), 
            'problem_count': exam_group.problem_count(),
            'exam_group': exam_group, 
            'exam_groups': ExamGroup.objects.all(),
            'finished_students': exam_group.finished_students().order_by('score'),
            'grades_distribution':  exam_group.grade_distribution(),
            'problem_distributions': exam_group.problem_distributions(),
            'tab_number': 1,
        }, context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_add_session(request): 
    return create_update.create_object(request, form_class=ExamGroupForm,
                                                            post_save_redirect="/admin/sessions/%(name)s", 
                                                            template_name="admin_session_add.html",
                                                            extra_context={'tab_number': 1})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_edit_session(request):
    # TODO: Edit session
    pass

@login_required
@user_passes_test(lambda u: u.is_staff)
@cache_page(60 * 5)
def admin_trends(request):
    # TODO: Trends
    return render_to_response("admin_trends.html", {'tab_number': 2}, context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_settings(request):
    the_exam = Exam.objects.all()[0]
    return create_update.update_object(request, form_class=ExamForm,
                                                object_id=the_exam.id,
                                                post_save_redirect="/admin/settings/", 
                                                template_name="admin_settings.html",
                                                extra_context={'tab_number': 3})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_student(request, student_id):
    if student_id:
        try:
            student = UserProfile.objects.get(student_id=student_id)
        except UserProfile.DoesNotExist:
            return HttpResponse("Error: No student with id " + student_id)
        except UserProfile.MultipleObjectsReturned:
            return HttpResponse("Error: Multiple students with id " + student_id)
    else:
        return HttpRespone("Error: No student id provided " + student_id)
    
    return render_to_response("admin_student.html", 
        {
            'student': student,
            'answer_sheets': student.answer_sheets(),
            'question_count': student.exam_group.problem_count(),
            'tab_number': 1,
        }, context_instance=RequestContext(request))
 