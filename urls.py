from django.conf.urls.defaults import *
from django.contrib.auth.views import login
import os.path
from django.conf import settings
from TUple.exam import views

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    (r'^$', login, {'template_name': 'home.html'}),
    (r'^didlogin/$', views.didlogin),
    (r'^instructions/$', views.instructions),
	(r'^popup/instructions/$', views.instructions, {'popup': True}),
    (r'^start/$', views.start),
    (r'^exam/$', views.exam),
	(r'^end/$', views.end),
    (r'^finished/$', views.finished),
    (r'^closed/$', views.closed),

	(r'^problem/(.+)/$', views.problem),
	(r'^hotkeys/(.+)/$', views.hotkeys),
	
	(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': settings.MEDIA_URL + 'images/favicon.ico'}),
    
    (r'^admin/$', views.admin),
    (r'^admin/sessions/$', views.admin_sessions),
    (r'^admin/sessions/add/$', views.admin_add_session),
    (r'^admin/sessions/(.+)/edit/$', views.admin_edit_session),
    (r'^admin/sessions/(.+)/$', views.admin_session),
    
    (r'^admin/trends/$', views.admin_trends),
    (r'^admin/settings/$', views.admin_settings),
    
    (r'^admin/distribution/(.+)/csv/$', views.distribution_csv),
    
    (r'^admin/grades/(.+)/csv/$', views.grades_csv),
    (r'^admin/grades/(.+)/$', views.grades),
    

    (r'^admin-django/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('', (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.dirname(__file__), 'media').replace('\\','/'), 'show_indexes': True}),
    )