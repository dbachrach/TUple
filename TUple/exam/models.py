from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, StdDev, Max, Min
from datetime import datetime, date
from django.forms import ModelForm


class Exam(models.Model):
    name = models.CharField(max_length=100)
    copyright_owner = models.CharField(max_length=100)
    copyright_start = models.PositiveSmallIntegerField()
    contact_email = models.EmailField()
    
    def __unicode(self):
        return u'%s' % (name)
        
    def copyright_end(self):
        return date.today().year
        
class ExamForm(ModelForm):
    class Meta:
        model = Exam

class Problem(models.Model):
    number = models.PositiveSmallIntegerField()
    text = models.TextField()
    
    class Meta:
        ordering = ('number',)
    
    def __unicode__(self):
        return u'Problem #%d' % (self.number)
        
    def sorted_answers(self):
        '''Returns the answers for this problem in sorted order (i.e. A, B, C, D, E).'''
        return self.answer_set.order_by('letter')
        

class ExamGroup(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    problems = models.ManyToManyField(Problem)
    examination_time = models.IntegerField(help_text="<em>minutes</em>")
    answers_per_problem = models.SmallIntegerField()
    active = models.BooleanField(help_text="<em>(Makes this the currently administered exam.</em>")
    
    class Meta:
        ordering = ('-date',)
            
    def __unicode__(self):
        return u'%s' % (self.name)
    
    def sorted_problems(self):
        '''Returns the problems for this group in their correct order.'''
        return self.problems.order_by('number')
        
    def finished_students(self):
        '''Returns the list of students in this group who have finished the exam.'''
        return self.userprofile_set.filter(test_status=2)
        
    def get_examination_time_string(self):
        return '%d minutes' % int(self.examination_time / 60)
    
    def problem_count(self):
        return self.sorted_problems().count()      
             
    def grade_distribution(self):
        problem_count = self.problem_count()
        return [[i, self.finished_students().filter(score=i).count()] for i in xrange(problem_count + 1)]
        
    def problem_distributions(self):
        '''Return a list of problems and each of its answers with the percentage of student responses for that answer.'''
        finished_students_count = self.finished_students().count()
        problem_distribution = []
        for problem in self.sorted_problems():
            answers = []
            response_count = 0
            for answer in problem.sorted_answers():
                chosen_count = answer.chosen_count_in_group(self)
                if finished_students_count > 0:
                    chosen_percentage = float(float(chosen_count) / float(finished_students_count) * 100.0)
                else:
                    chosen_percentage = 0.0
                answers.append({'answer': answer, 
                                'chosen_count': chosen_count, 
                                'chosen_percentage': chosen_percentage})
                
                response_count += chosen_count
            
            unanswered_count = finished_students_count - response_count
            if finished_students_count > 0:    
                unanswered_percentage = float(float(unanswered_count) / float(finished_students_count) * 100.0)
            else:
                unanswered_percentage = 0.0
            problem_distribution.append({'problem': problem, 
                                         'answers': answers, 
                                         'unanswered_count': unanswered_count,
                                         'unanswered_percentage': unanswered_percentage})
        return problem_distribution
        
    def calculate_statistics(self):
        '''Calculates various statistics for this exam group. The statistics are returned as an dictionary of statistic names to values.
           The statistics available are:
                question_count, finished_students_count, current_students_count, unstarted_students_count, total_students_count, 
                finished_students_percentage, current_students_percentage, unstarted_students_percentage,
                standard_deviation, average_score, high_score, low_score, average_score_percentage, high_score_percentage, low_score_percentage'''
                
        question_count = self.problems.count()
        total_students_count = self.userprofile_set.count()
        
        if question_count == 0 or total_students_count == 0:
            return None
        
        finished_students = self.finished_students()
        
        finished_students_count = finished_students.count()
        current_students_count = self.userprofile_set.filter(test_status=1).count()
        unstarted_students_count = self.userprofile_set.filter(test_status=0).count()
        
        
        finished_students_percentage = float(finished_students_count) / float(total_students_count) * 100
        current_students_percentage = float(current_students_count) / float(total_students_count) * 100
        unstarted_students_percentage = float(unstarted_students_count) / float(total_students_count) * 100
        
        if finished_students:
            __aggregates = finished_students.aggregate(average_score=Avg('score'), high_score=Max('score'), low_score=Min('score'))
            average_score = int(__aggregates['average_score'])
            
            # Standard deviation is not available in Sqlite
            if 'standard_deviation' in __aggregates:
                standard_deviation = __aggregates['standard_deviation'] 
            else:
                standard_deviation = ""
                
            high_score = __aggregates['high_score']
            low_score = __aggregates['low_score']
            
            average_score_percentage = float(average_score) / float(question_count) * 100
            high_score_percentage = float(high_score) / float(question_count) * 100
            low_score_percentage = float(low_score) / float(question_count) * 100
        return locals()
    
class ExamGroupForm(ModelForm):
    class Meta:
        model = ExamGroup
        exclude = ('problems',)
                
class UserProfile(models.Model):
    student_id = models.CharField(max_length=20)
    test_status = models.SmallIntegerField() # 0 = Not Started, 1 = In Progress, 2 = Finished
    score = models.IntegerField(default=0)
    test_date = models.DateTimeField(null=True)
    exam_group = models.ForeignKey(ExamGroup)
    problems = models.ManyToManyField(Problem, through='AnswerSheet')
    user = models.ForeignKey(User, unique=True) # Correlate this to the User table. This lets us extend properties of authenticated users.
    retake= models.BooleanField()
    
    def __unicode__(self):
        return u'UserProfile (%s)' % (self.user)
        
    def has_not_started(self):
        '''Returns True if the user has not begun the exam.'''
        return (self.test_status == 0)
    
    def is_in_progress(self):
        '''Returns True if the user is currently taking the exam.'''
        return (self.test_status == 1)
        
    def has_finished(self):
        '''Returns True if the user has compoleted the exam.'''
        return (self.test_status == 2)
        
    def is_in_active_exam_group(self):
        '''Returns True if the user is in the active exam group. A user must be in an active exam group to take an exam.'''
        return (self.exam_group.active)
        
    def is_allowed_to_test(self):
        '''Returns True if the user can take an exam. A user must be either in the active exam group or have the retake priveledge.'''
        return (self.is_in_active_exam_group() or self.retake)
    
    def time_left(self):
        '''Returns how much time the user has before his/her exam will be turned in.'''
        exam_time = self.exam_group.examination_time
        
        time_difference = (datetime.now() - self.test_date).total_seconds()
        if time_difference > exam_time:
            self.end_exam()
            return -1
            
        return int(exam_time - time_difference)
        
    def start_exam(self):
        '''Marks the user as currently in progress. The current time is also recorded as the start date for the user.
           A user must have not started the exam for these actions to take effect.'''
        if self.has_not_started():
            self.test_status = 1
            self.test_date = datetime.now()
            self.save()
        
    def end_exam(self):
        '''Marks the user as finished, and the user's score is calculated.
           A user must be currently in progress for these actions to take effect.'''
        if self.is_in_progress():
            self.update_score()
            self.test_status = 2
            self.retake = False
            self.save()
    
    def get_problem_at_number(self, problem_number):
        '''Returns Problem #x. If no problem is found at this number, returns None.
           The user is authorized to view and answer the returned problem.'''
        try:
            problem = self.problems.get(number=problem_number)
            return problem
        except Problem.DoesNotExist, Problem.MultipleObjectsReturned:
            return None
                    
    def get_answer_for_problem(self, problem):
        '''Returns the user's answer for the given problem.'''
        try:    
            answer_sheet = AnswerSheet.objects.get(user_profile=self, problem=problem)
        except AnswerSheet.DoesNotExist, AnswerSheet.MultipleObjectsReturned:
            return None
        
        return answer_sheet.answer

    def answer_sheets(self):
        try:    
            answer_sheets = AnswerSheet.objects.filter(user_profile=self)
        except AnswerSheet.DoesNotExist:
            return None
        return answer_sheets
        
    def answer_problem(self, problem, answer):
        '''Marks the user's response to problem as answer. A user must be currently taking the exam.''' 
        if not self.is_in_progress():
            return
        if self.time_left() == -1:
            return
        
        try:    
            answer_sheet = AnswerSheet.objects.get(user_profile=self, problem=problem)
        except AnswerSheet.DoesNotExist, AnswerSheet.MultipleObjectsReturned:
            return
        
        answer_sheet.answer = answer
        answer_sheet.save()
        
    def update_score(self):
        '''Calculates the user's score, saves it to UserProfile.score and returns the score.'''     
        new_score = AnswerSheet.objects.filter(user_profile=self, answer__correct=True).count()
        self.score = new_score
        self.save()
        return new_score
        
    def can_retake(self):
        return self.retake
        
    def give_retake(self):
        self.retake = True
        self.test_status = 0
        self.test_date = None
        self.save()


class Answer(models.Model):
    letter = models.CharField(max_length=4)
    text = models.TextField()
    correct = models.BooleanField()
    problem = models.ForeignKey(Problem)
    
    def __unicode__(self):
        return u'Answer %s' % (self.letter)
    
    def chosen_count_in_group(self, group):
        '''Returns the number of times this answer choice was chosen for a given exam group.'''
        return AnswerSheet.objects.filter(problem=self.problem,
                                          answer=self,
                                          user_profile__exam_group=group,
                                          user_profile__test_status=2).count()
            
    
class AnswerSheet(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    problem = models.ForeignKey(Problem)
    answer = models.ForeignKey(Answer, null=True)
    
    def __unicode__(self):
        return u'Sheet (%s, %s)' % (self.user_profile, self.problem)
        