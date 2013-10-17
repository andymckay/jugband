from django.conf.urls.defaults import *

from . import views


urlpatterns = patterns('',
    url(r'^$', views.home, name='engineering.home'),
    url(r'^bugs.json$', views.json_bugs, name='engineering.json_bugs'),
)
