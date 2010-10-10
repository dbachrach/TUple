from django.conf.urls.defaults import *
from django.contrib.auth.views import login
import os.path
from django.conf import settings
from TUple.exam import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^placement/', include('placement.foo.urls')),

    (r'^$', login, {'template_name' : 'home.html'}),
    (r'^instructions/$', views.instructions),
    (r'^start/$', views.start),
    (r'^exam/$', views.exam),
    (r'^finished/$', views.finished),
    (r'^closed/$', views.closed),
    
    

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('', (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.dirname(__file__), 'media').replace('\\','/'), 'show_indexes': True}),
    )