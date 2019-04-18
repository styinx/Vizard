from django.urls import path, re_path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^(?:(?P<api>\w+)/)?data/(?:(?P<_id>\w+)/)?$', views.data, name='data'),
    re_path(r'^report/(?:(?P<_id>\w+)/)(?:(?P<export>\w+)/)?$', views.report_id, name='report_id')
]
#(?:(?P<export>\w+)/)?