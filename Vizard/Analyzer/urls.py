from django.urls import path, re_path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^tasks/(?:(?P<api>\w+)/)?$', views.tasks, name='tasks'),
    re_path(r'^loadtest/(?:(?P<tool>\w+)/)(?:(?P<api>\w+)/)?$', views.loadtest, name='loadtest'),
    re_path(r'^stresstest/(?:(?P<tool>\w+)/)?(?:(?P<api>\w+)/)?$', views.stresstest, name='stresstest')
]
