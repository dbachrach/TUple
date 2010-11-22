from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from exam_settings import EXAM_SETTINGS
from django.template import RequestContext
from django.utils import simplejson
from django.contrib import messages
from TUple.exam.models import Problem, ExamGroup, Answer, Exam, ExamForm, UserProfile
import csv

import logging
LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
    
# TODO: Make admins have a user profile

# TODO: Handle retakes
def check_closed(f):
    def _inner(*args, **kwargs):
        if EXAM_SETTINGS['exam_closed']:
            return closed(*args, **kwargs)
        else:
            return f(*args, **kwargs)
    return _inner


@check_closed
@login_required
def didlogin(request):
    if request.user.is_staff:
        return HttpResponseRedirect('/admin/')
    if not request.user.get_profile().is_in_active_exam_group():
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
    return render_to_response("instructions.html", {'popup': popup, 'problem_count': problem_count, 'exam_length': exam_length}, context_instance=RequestContext(request))


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
    
    exam_answers_per_problem = 5 # TODO: exam_group.answers_per_problem
    
    # Creates a list of each problem's selected answer
    chosen_answers = map(request.user.get_profile().get_answer_for_problem, problems)

    # Combines the problems and their chosen answer into a single list where each element is a dictionary containting the problem and the selected answer
    problem_data = map(lambda p, c : {'problem': p, 'chosen_answer': c}, problems, chosen_answers)
    
    return render_to_response("exam.html", {'problem_data': problem_data, 'time_left': time_left, 'exam_answers_per_problem': exam_answers_per_problem}, context_instance=RequestContext(request))


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
        # TODO: Better error
        return HttpResponse("Problem not found")
        
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
        # TODO: Better error
        return HttpResponse("Problem not found")

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
    chosen_answer = request.user.get_profile().get_answer_for_problem(problem)
    return render_to_response("problem.html", {'problem': problem, 'chosen_answer': chosen_answer}, context_instance=RequestContext(request))

    
@check_closed
@login_required 
def post_problem(request, problem):
    if 'answer' in request.POST and request.POST['answer']:
        answer_id = request.POST['answer']
        try:
            answer = Answer.objects.get(id=answer_id) 
        except Answer.DoesNotExist:
            # TODO: Return error
            return HttpResponse("error: no active group exists")
        except Answer.MultipleObjectsReturned:
            # TODO: Return error
            return HttpResponse("error: multiple active groups exist")
        
        # Ensure the user has provided an appropriate answer to the problem.
        if problem != answer.problem:
            # TODO: Error
            return HttpResponse("Error: problem != answer.problem")
            
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
        # TODO: Return error
        return HttpResponse("error: no active group exists")
    except ExamGroup.MultipleObjectsReturned:
        # TODO: Return error
        return HttpResponse("error: multiple active groups exist")
    return HttpResponseRedirect('/admin/sessions/' + exam_group.name + '/')
            
    
@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_session(request, group_name):
    if group_name:
        try:
            exam_group = ExamGroup.objects.get(name=group_name)
        except ExamGroup.DoesNotExist:
            # TODO: Return error
            return HttpResponse("error: no group with name " + group_name)
        except ExamGroup.MultipleObjectsReturned:
            # TODO: Return error
            return HttpResponse("error: multiple groups with name " + group_name)
    else:
        # TODO: Return error
        return HttpRespone("error: no group name provided " + group_name)
    
    return render_to_response("admin_session.html", 
        {
            'stats': exam_group.calculate_statistics(), 
            'problems': exam_group.sorted_problems(), 
            'problem_count': exam_group.problem_count(),
            'exam_group': exam_group, 
            'exam_groups': ExamGroup.objects.all(), 
            'finished_students': exam_group.finished_students().order_by('score'),
            'grades_distribution':  exam_group.grade_distribution(),
        }, context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_add_session(request):
    pass

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_edit_session(request):
    pass

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_trends(request):
    pass

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_settings(request):
    the_exam = Exam.objects.all()[0]
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=the_exam)
        if form.is_valid():
            form.save()
            messages.info(request, 'Settings saved.')
            return HttpResponseRedirect("/admin/settings/?saved")
    else:
        form = ExamForm(instance=the_exam)

    return render_to_response("admin_settings.html", {'form': form}, context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_student(request, student_id):
    if student_id:
        try:
            student = UserProfile.objects.get(id=student_id)
        except UserProfile.DoesNotExist:
            # TODO: Return error
            return HttpResponse("error: no student with id " + student_id)
        except UserProfile.MultipleObjectsReturned:
            # TODO: Return error
            return HttpResponse("error: multiple students with id " + student_id)
    else:
        # TODO: Return error
        return HttpRespone("error: no student id provided " + student_id)
    
    return render_to_response("admin_student.html", 
        {
            'student': student,
            'answer_sheets': student.answer_sheets(),
        }, context_instance=RequestContext(request))
            
# @login_required
# @user_passes_test(lambda u: u.is_staff)
# def distribution_csv(request, group):
#     response = HttpResponse(mimetype='text/csv')
#     response['Content-Disposition'] = 'attachment; filename=distribution.csv'
#     
#     writer = csv.writer(response)
#     # TODO: Handle 4 and 5 answers (A,B,C,D and A,B,C,D,E)
#     writer.writerow(['Problem Number', 'Question', 'A', 'B', 'C', 'D', 'E', 'Unanswered', 'Correct'])
#     
#     # TODO: Write distributions
#     
#     return response
#     
#     
# @login_required
# @user_passes_test(lambda u: u.is_staff)
# def grades_csv(request, group_name):
#     try:
#         exam_group = ExamGroup.objects.get(name=group_name)
#     except ExamGroup.DoesNotExist:
#         # TODO: Return error
#         return HttpResponse("error: no group with name " + group_name)
#     except ExamGroup.MultipleObjectsReturned:
#         # TODO: Return error
#         return HttpResponse("error: multiple groups with name " + group_name)
#         
#     response = HttpResponse(mimetype='text/csv')
#     response['Content-Disposition'] = 'attachment; filename=grades.csv'
#     
#     writer = csv.writer(response)
#     writer.writerow(['Name', 'Score'])
#     
#     for student in exam_group.finished_students().order_by(user__username):
#         writer.writerow([student.user.username, student.score])
#     
#     return response
# 
# 
# @login_required
# @user_passes_test(lambda u: u.is_staff)
# def grades(request, group_name):
#     try:
#         exam_group = ExamGroup.objects.get(name=group_name)
#     except ExamGroup.DoesNotExist:
#         # TODO: Return error
#         return HttpResponse("error: no group with name " + group_name)
#     except ExamGroup.MultipleObjectsReturned:
#         # TODO: Return error
#         return HttpResponse("error: multiple groups with name " + group_name)
#         
#     return render_to_response("admin_grades.html", {'finished_students': exam_group.finished_students().order_by('score')}, context_instance=RequestContext(request))
    