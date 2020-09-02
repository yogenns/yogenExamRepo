import datetime
from django.views.generic.edit import FormView
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, CreateView, DeleteView, ListView, View, DetailView
from django.urls import reverse_lazy
from . import forms
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect

# Create your views here.


class HomeView(TemplateView):
    template_name = 'exam_app/home.html'

    def get_context_data(self, **kwargs):

        if self.request.user.is_authenticated:
            if not self.request.user.is_superuser:
                # If user is authenticated and is NOT a super user show exam list
                kwargs['exam_list'] = models.Exam.objects.all().order_by('pk')
        return super(HomeView, self).get_context_data(**kwargs)


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
        answer_list = form.cleaned_data.get('answer')
        question.answer = list(answer_list.split(','))
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
        exam_id = self.request.GET.get("exam_id")
        if exam_id != '' and exam_id != None:
            return models.Question.objects.filter(exam=exam_id).order_by('pk')
        else:
            return models.Question.objects.all().order_by('pk')


class DeleteQuestionView(SuperUserRequiredMixin, DeleteView):
    model = models.Question
    success_url = reverse_lazy('exam_app:questions')

    def get_queryset(self):
        queryset = super().get_queryset()
        selected_list = self.request.POST.get("selectedRows").split(',')
        if 'all' in selected_list:
            return queryset
        else:
            print(selected_list)
            return queryset.filter(pk__in=selected_list)

    def delete(self, *args, **kwargs):
        questions = self.get_queryset()
        print("Deleting Questions")
        print(questions)
        questions.delete()
        return HttpResponseRedirect('/questions/')


class CreateExamView(SuperUserRequiredMixin, FormView):
    form_class = forms.CreateExamForm
    success_url = reverse_lazy('exam_app:create_exam')
    template_name = 'exam_app/add_exam.html'
    success_message = "Success YY"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Exam Added successfully')
        return super().form_valid(form)


class ListExamView(SuperUserRequiredMixin, ListView):
    model = models.Exam
    paginate_by = 10

    def get_queryset(self):
        return models.Exam.objects.all().order_by('pk')


class DeleteExamView(SuperUserRequiredMixin, DeleteView):
    model = models.Exam
    success_url = reverse_lazy('exam_app:exams')

    def get_queryset(self):
        queryset = super().get_queryset()
        selected_list = self.request.POST.get("selectedRows").split(',')
        if 'all' in selected_list:
            return queryset
        else:
            print(selected_list)
            return queryset.filter(pk__in=selected_list)

    def delete(self, *args, **kwargs):
        exams = self.get_queryset()
        print("Deleting Exams")
        print(exams)
        exams.delete()
        return HttpResponseRedirect('/exams/')


class StartExamView(LoginRequiredMixin, TemplateView):
    template_name = 'exam_app/start_exam.html'

    def post(self, request, **kwargs):
        exam_id = request.POST.get('exam-id')
        context = self.get_context_data()
        exam_obj = get_object_or_404(models.Exam, pk=exam_id)
        exam_attempt = models.ExamAttempt()
        exam_attempt.start_time = datetime.datetime.now()
        exam_attempt.end_time = datetime.datetime.now()
        exam_attempt.exam = exam_obj
        exam_attempt.user = self.request.user
        exam_attempt.save()
        context['exam_obj'] = exam_obj
        context['exam_attempt_id'] = exam_attempt.pk
        return render(request, self.template_name, context)

    def get(self, request, **kwargs):
        return HttpResponseRedirect('/')


class SubmitExamView(LoginRequiredMixin, View):

    def post(self, request, **kwargs):
        exam_attempt_id = request.POST.get('exam_attempt_id')
        exam_attempt_obj = get_object_or_404(
            models.ExamAttempt, pk=exam_attempt_id)
        exam_attempt_obj.end_time = datetime.datetime.now()
        # Set the Anwser List Here.
        # {'que_id':['ans1','ans2'],}
        answer_dict = {}
        result_attempted_question_count = 0
        result_correct_answer_count = 0
        for question in exam_attempt_obj.exam.questions.all():
            ans_list = request.POST.getlist(str(question.pk))

            if len(ans_list) > 0:
                result_attempted_question_count += 1
                ans_list.sort()
                actual_ans = eval(question.answer)
                if actual_ans == ans_list:
                    result_correct_answer_count += 1

            answer_dict[question.pk] = ans_list
        exam_attempt_obj.answer_list = answer_dict

        # Perform Analysis
        exam_attempt_obj.result_attempted_question_count = result_attempted_question_count
        exam_attempt_obj.result_correct_answer_count = result_correct_answer_count
        exam_attempt_obj.result_percentage = (
            result_correct_answer_count / exam_attempt_obj.exam.question_count) * 100
        print("resPecentage "+str(exam_attempt_obj.result_percentage))
        print("resCorrect "+str(exam_attempt_obj.result_correct_answer_count))
        print("resAttempted "+str(exam_attempt_obj.result_attempted_question_count))
        passing_percentage = exam_attempt_obj.exam.passing_percentage

        if exam_attempt_obj.result_percentage >= passing_percentage:
            exam_attempt_obj._result_status = 'P'
        else:
            exam_attempt_obj._result_status = 'F'

        exam_attempt_obj.save()
        return HttpResponseRedirect('/user/result/'+str(exam_attempt_id))

    def get(self, request, **kwargs):
        return HttpResponseRedirect('/')


class ViewExamResultDetailView(LoginRequiredMixin, DetailView):
    model = models.ExamAttempt
    template_name = 'exam_app/result_detail.html'

    def get_queryset(self):
        #user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(pk=self.kwargs.get('pk'))
        return queryset
