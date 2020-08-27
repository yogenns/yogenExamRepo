from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'exam_app'

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url('login/', auth_views.LoginView.as_view(template_name='exam_app/login.html'), name='login'),
    url('logout/', auth_views.LogoutView.as_view(), name='logout'),
    url('signup/', views.SignUp.as_view(), name='signup'),
    url('topic/', views.CreateTopicView.as_view(), name='topic'),
]
