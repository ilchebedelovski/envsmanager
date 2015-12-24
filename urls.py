from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from localenvs.login import Login
from localenvs.login import Logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'envsmanager.views.home', name='home'),
    # url(r'^envsmanager/', include('envsmanager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^localenvs/dashboard/$', 'localenvs.views.dashboard'),
    url(r'^localenvs/formresolution/$', 'localenvs.views.formresolution'),
    url(r'^localenvs/removeenv/$', 'localenvs.views.removeenv'),
    url(r'^localenvs/removesuccess/$', 'localenvs.views.removeSuccess'),
    url(r'^localenvs/importenv/$', 'localenvs.views.importenv'),
    url(r'^localenvs/backupenv/$', 'localenvs.views.backupenv'),
    url(r'^localenvs/gitenv/$', 'localenvs.views.gitenv'),
    url(r'^localenvs/$', Login.as_view()),
    url(r'^localenvs/logout/$', Logout.as_view())    
  
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()