#from django.conf import settings
from exam_settings import SETTINGS

#def media_url(request):
#    return {'media_url': settings.MEDIA_URL}
    
def exam_settings(request):
    return SETTINGS