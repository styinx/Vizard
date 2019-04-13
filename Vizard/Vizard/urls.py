from django.contrib import admin
from django.urls import include, path

from . import views


urlpatterns = [
    path('', views.index, name='index'),

    path('home/', views.index, name='index'),
    path('details/', views.details, name='details'),
    path('documentation/', views.documentation, name='documentation'),

    path('admin/', admin.site.urls),
    path('analyze/', include('Analyzer.urls')),
    path('present/', include('Presenter.urls')),
]
