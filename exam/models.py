from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, StdDev, Max, Min


class Problem(models.Model):
	number = models.PositiveSmallIntegerField()
	text = models.TextField()

class ExamGroup(models.Model):
	name = models.TextField()
	date = models.DateField()
	active = models.BooleanField()
	problems = models.ManyToManyField(Problem)
	
	def finished_students(self):
	    return self.userprofile_set.filter(test_status=2)
	    
	    
	def calculate_statistics(self):
		'''Calculates various statistics for this exam group. The statistics are returned as an dictionary of statistic names to values.
			The statistics available are:
		   		question_count, finished_students_count, current_students_count, unstarted_students_count, total_students_count, 
		   		finished_students_percentage, current_students_percentage, unstarted_students_percentage,
		   		standard_deviation, average_score, high_score, low_score, average_score_percentage, high_score_percentage, low_score_percentage'''
		   		
		question_count = self.problems.count()
		finished_students = self.finished_students()
		
		finished_students_count = finished_students.count()
		current_students_count = self.userprofile_set.filter(test_status=1).count()
		unstarted_students_count = self.userprofile_set.filter(test_status=0).count()
		total_students_count = self.userprofile_set.count()
		
		finished_students_percentage = float(finished_students_count) / float(total_students_count) * 100
		current_students_percentage = float(current_students_count) / float(total_students_count) * 100
		unstarted_students_percentage = float(unstarted_students_count) / float(total_students_count) * 100
		
		if finished_students:
			__aggregates = finished_students.aggregate(average_score=Avg('score'), high_score=Max('score'), low_score=Min('score'))
			average_score = int(__aggregates['average_score'])
			# TODO: (Doesnt work on sqlite) standard_deviation = __aggregates['standard_deviation']    standard_deviation=StdDev('score'),
			high_score = __aggregates['high_score']
			low_score = __aggregates['low_score']
			
			average_score_percentage = float(average_score) / float(question_count) * 100
			high_score_percentage = float(high_score) / float(question_count) * 100
			low_score_percentage = float(low_score) / float(question_count) * 100
		return locals()
	

class UserProfile(models.Model):
    test_status = models.SmallIntegerField() # 0 = Not Started, 1 = In Progress, 2 = Finished
    score = models.IntegerField(default=0)
    test_date = models.DateTimeField()
    exam_group = models.ForeignKey(ExamGroup)
    problems = models.ManyToManyField(Problem, through='AnswerSheet')
    
    # Correlate this to the User table. This lets us extend properties of authenticated users.
    user = models.ForeignKey(User, unique=True)
    
    def answer_problem(problem, answer):
        x = 1 # TODO: Write this method
        
    def get_score(self):
    	''' Calculates the user's score, saves it to UserProfile.score and returns the score.'''
    	score = 0
    	score = self.answer_sheet.filter(correct=True).count()
#    	for answer_sheet in self.answersheet_set.all():
#    		if answer_sheet.answer.correct:
#    			score = score + 1
    	self.score = score
    	self.save() # TODO: We need this right?
    	return score


class Answer(models.Model):
	letter = models.CharField(max_length=4)
	text = models.TextField()
	correct = models.BooleanField()
	problem = models.ForeignKey(Problem)
	
class AnswerSheet(models.Model):
	user_profile = models.ForeignKey(UserProfile)
	problem = models.ForeignKey(Problem)
	answer = models.ForeignKey(Answer)
		


