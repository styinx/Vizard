from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('data/', views.data, name='data'),
    path('data/<str:_id>/', views.data_id, name='data'),
    path('report/', views.report, name='report'),
    path('report/<int:_id>/', views.report_id, name='report')
]
