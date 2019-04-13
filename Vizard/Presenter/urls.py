from django.urls import path, re_path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^(?:(?P<api>\w+)/)?data/(?:(?P<_id>\w+)/)?$', views.data, name='data'),
    path('report/<str:_id>/', views.report_id, name='report_id')
]
