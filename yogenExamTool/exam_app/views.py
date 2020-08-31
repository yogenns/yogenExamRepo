from django.views.generic.edit import FormView
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DeleteView, ListView
from django.urls import reverse_lazy
from . import forms
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect

# Create your views here.


class HomeView(TemplateView):
    template_name = 'exam_app/home.html'


class SignUp(CreateView):
    form_class = forms.CreateUserForm
    success_url = reverse_lazy('exam_app:login')
    template_name = 'exam_app/signup.html'


class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser


class CreateTopicView(SuperUserRequiredMixin, CreateView):
    form_class = forms.CreateTopicForm
    success_url = reverse_lazy('exam_app:topic')
    template_name = 'exam_app/topic.html'

    def get_context_data(self, **kwargs):
        kwargs['topic_list'] = models.Topic.objects.order_by('id')
        return super(CreateTopicView, self).get_context_data(**kwargs)


class DeleteTopicView(SuperUserRequiredMixin, DeleteView):
    model = models.Topic
    success_url = reverse_lazy('exam_app:topic')

    def get_queryset(self):
        queryset = super().get_queryset()
        selected_list = self.request.POST.get("selectedRows").split(',')
        if 'all' in selected_list:
            return queryset
        else:
            print(selected_list)
            return queryset.filter(pk__in=selected_list)

    def delete(self, *args, **kwargs):
        topics = self.get_queryset()
        print("Deleting Topic")
        print(topics)
        topics.delete()
        return HttpResponseRedirect('/topic/')


class CreateQuestionView(SuperUserRequiredMixin, FormView):
    form_class = forms.CreateQuestionForm
    success_url = reverse_lazy('exam_app:create_question')
    template_name = 'exam_app/add_question.html'

    def form_valid(self, form):
        question = models.Question()
        question.question = form.cleaned_data.get('question')
        question.answer = form.cleaned_data.get('answer')
        question._question_type = form.cleaned_data.get('question_type')
        question.topic = form.cleaned_data.get('topic')
        question.explaination = form.cleaned_data.get('explaination')
        options = {}
        options['A'] = form.cleaned_data.get('option_field_A')
        options['B'] = form.cleaned_data.get('option_field_B')
        if form.cleaned_data.get('option_field_C') != '':
            options['C'] = form.cleaned_data.get('option_field_C')
        if form.cleaned_data.get('option_field_D') != '':
            options['D'] = form.cleaned_data.get('option_field_D')
        if form.cleaned_data.get('option_field_E') != '':
            options['E'] = form.cleaned_data.get('option_field_E')
        if form.cleaned_data.get('option_field_F') != '':
            options['F'] = form.cleaned_data.get('option_field_F')
        question.options = options
        print(question)
        question.save()
        messages.success(self.request, 'Question Added successfully')
        return super().form_valid(form)


class ListQuestionView(SuperUserRequiredMixin, ListView):
    model = models.Question
    paginate_by = 10

    def get_queryset(self):
        return models.Question.objects.all().order_by('pk')
