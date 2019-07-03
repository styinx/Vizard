from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import include, path, re_path

from . import views


urlpatterns = [
    path('', views.home, name='index'),

    path('home/', views.home, name='index'),
    path('details/', views.details, name='details'),
    path('documentation/', views.documentation, name='documentation'),
    path('bot/', views.bot, name='bot'),
    path('demo/', views.demo, name='demo'),
    path('webhook/', csrf_exempt(views.webhook), name='webhook'),
    re_path(r'^my/(?:(?P<what>\w+)/)?$', views.my, name='my'),

    path('admin/', admin.site.urls),
    path('analyze/', include('Analyzer.urls')),
    path('present/', include('Presenter.urls')),

    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.ico')),
]
