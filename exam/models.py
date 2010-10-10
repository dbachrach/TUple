from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    test_status = models.SmallIntegerField()
    score = models.IntegerField()
    answers = models.TextField()
    test_date = models.DateTimeField()
    class_year = models.IntegerField()
    user = models.ForeignKey(User, unique=True)

class Problem(models.Model):
    ANSWER_CHOICES = (
        (u'A', u'A'),
        (u'B', u'B'),
        (u'C', u'C'),
        (u'D', u'D'),
        (u'E', u'E'),
    )
    question = models.TextField()
    solution_a = models.TextField()
    solution_b = models.TextField()
    solution_c = models.TextField()
    solution_d = models.TextField()
    solution_e = models.TextField()
    correct_solution = models.CharField(max_length=1, choices=ANSWER_CHOICES)

