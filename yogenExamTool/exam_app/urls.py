from django.conf.urls import url
from . import views

app_name = 'exam_app'

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
]
