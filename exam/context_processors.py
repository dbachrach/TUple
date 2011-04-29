from django.conf import settings
from TUple.exam.models import Exam
from django.core import serializers

def media_url(request):
    return {'media_url': settings.MEDIA_URL}

def exam_attrs(request):
    the_exam = Exam.objects.all()[0]
    data = serializers.serialize('python', Exam.objects.all())[0]['fields']
    data['copyright_end'] = the_exam.copyright_end()
    return data
