from django.contrib import admin
from django.urls import include, path, re_path

from . import views


urlpatterns = [
    path('', views.home, name='index'),

    path('home/', views.home, name='index'),
    path('details/', views.details, name='details'),
    path('documentation/', views.documentation, name='documentation'),
    re_path(r'^my/(?:(?P<what>\w+)/)?$', views.my, name='my'),

    path('admin/', admin.site.urls),
    path('analyze/', include('Analyzer.urls')),
    path('present/', include('Presenter.urls')),
]
