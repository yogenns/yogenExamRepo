from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'exam_app'

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url('login/', auth_views.LoginView.as_view(template_name='exam_app/login.html'), name='login'),
    url('logout/', auth_views.LogoutView.as_view(), name='logout'),
    url('signup/', views.SignUp.as_view(), name='signup'),
    url('^topic/$', views.CreateTopicView.as_view(), name='topic'),
    url('^topic/delete/$', views.DeleteTopicView.as_view(), name='topic_delete'),
    url('^question/add/$', views.CreateQuestionView.as_view(), name='create_question'),
    url('^questions/$', views.ListQuestionView.as_view(), name='questions'),
    url('^question/delete/$', views.DeleteQuestionView.as_view(),
        name='question_delete'),
    url('^exam/add/$', views.CreateExamView.as_view(), name='create_exam'),
    url('^exams/$', views.ListExamView.as_view(), name='exams'),
    url('^exam/delete/$', views.DeleteExamView.as_view(), name='exam_delete'),
    url('^start/$', views.StartExamView.as_view(), name='exam_start'),
    url('^submit_exam/$', views.SubmitExamView.as_view(), name='submit_exam'),
    url('^user/result/(?P<pk>\d+)/$',
        views.ViewExamResultDetailView.as_view(), name='view_result'),
    url('^history/$', views.ListExamAttemptHistoryView.as_view(), name='history'),
    url('^user/result/detail/(?P<pk>\d+)/$',
        views.ViewExamResultMoreDetailView.as_view(), name='view_result_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
