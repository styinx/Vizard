from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('jobs', views.jobs, name='jobs'),
    path('loadtest/', views.loadtest, name='loadtest'),
    path('jmeter/', views.loadtest_jmeter, name='jmeter'),
    path('locust/', views.loadtest_locust, name='locust'),
    path('stresstest/', views.stresstest, name='stresstest')
]
