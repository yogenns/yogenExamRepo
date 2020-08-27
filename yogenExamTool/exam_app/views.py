from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from . import forms
from . import models

# Create your views here.


class HomeView(TemplateView):
    template_name = 'exam_app/home.html'


class SignUp(CreateView):
    form_class = forms.CreateUserForm
    success_url = reverse_lazy('exam_app:login')
    template_name = 'exam_app/signup.html'


class CreateTopicView(CreateView):
    form_class = forms.CreateTopicForm
    success_url = reverse_lazy('exam_app:topic')
    template_name = 'exam_app/topic.html'

    def get_context_data(self, **kwargs):
        kwargs['topic_list'] = models.Topic.objects.order_by('id')
        return super(CreateTopicView, self).get_context_data(**kwargs)
