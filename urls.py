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
    (r'^didlogin/$', views.didlogin),
    (r'^instructions/$', views.instructions),
	(r'^popup/instructions/$', views.instructions, {'popup' : True}),
    (r'^start/$', views.start),
    (r'^exam/$', views.exam),
	(r'^end/$', views.end),
    (r'^finished/$', views.finished),
    (r'^closed/$', views.closed),

	(r'^problem/(.+)/$', views.problem),
	
	(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/media/images/favicon.ico'}),
    
    

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('', (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.dirname(__file__), 'media').replace('\\','/'), 'show_indexes': True}),
    )