from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('tasks', views.tasks, name='tasks'),
    path('loadtest/', views.loadtest, name='loadtest'),
    path('loadtest/jmeter/', views.loadtest_jmeter, name='jmeter'),
    path('loadtest/locust/', views.loadtest_locust, name='locust'),
    path('stresstest/', views.stresstest, name='stresstest')
]
