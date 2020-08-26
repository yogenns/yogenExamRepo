from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'exam_app'

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url('login/', auth_views.LoginView.as_view(template_name='exam_app/login.html'), name='login'),
]
