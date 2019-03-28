from django.contrib import admin
from django.urls import include, path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('user/<str:_user>/', views.user, name='user'),
    path('admin/', admin.site.urls),
    path('analyze/', include('Analyzer.urls')),
    path('present/', include('Presenter.urls')),
]
