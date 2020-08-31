import random
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Topic, Question, Exam


class CreateUserForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1')
        model = get_user_model()


class CreateTopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'textinputclass'}),
        }


class CreateQuestionForm(forms.Form):
    QUESTION_TYPES = (
        ('', '----'),
        ('M', 'Multiple Selection'),
        ('S', 'Single Selection')
    )
    question = forms.CharField(widget=forms.Textarea)
    option_field_A = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Option'}), label="Option 'A'")
    option_field_B = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Option'}), label="Option 'B'")
    option_field_C = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Option'}), label="Option 'C'", required=False)
    option_field_D = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Option'}), label="Option 'D'", required=False)
    option_field_E = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Option'}), label="Option 'E'", required=False)
    option_field_F = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Option'}), label="Option 'F'", required=False)

    answer = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Answer e.g. A,C'}), label="Answers (Enter the Option Label. In case of multiple separate by comma)")
    question_type = forms.ChoiceField(choices=QUESTION_TYPES)
    topic = forms.ModelChoiceField(queryset=Topic.objects.all())
    explaination = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Provide Explaination'}))


class CreateExamForm(forms.ModelForm):

    SELECTION_TYPES = (
        ('', '----'),
        ('R', 'Random Selection From All'),
        ('RT', 'Random Selection From Selected Topic'),
        ('RU', 'Random Selection From Unused Questions'),
        ('RUT', 'Random Selection From Unused Questions From Selected Topic'),
    )
    topic = forms.ModelMultipleChoiceField(
        required=False, queryset=Topic.objects.all())
    question_selection = forms.ChoiceField(required=False,
                                           label="Question Selection Criteria", choices=SELECTION_TYPES)
    questions = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Question.objects.all()
    )

    class Meta:
        model = Exam
        fields = ('name', 'question_count',
                  'time', 'passing_percentage', 'questions')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'textinputclass'}),
            'time': forms.TimeInput(format='%H:%M', attrs={'placeholder': 'Enter Time (Hour:Minutes) e.g. 1:20'},),
        }

    def save(self, commit=True, *args, **kwargs):
        data = self.cleaned_data
        if data['question_selection'] == '' and not data['questions'].exists():
            raise ValidationError(
                {'question_selection': ["Either Select Questions Or Select a Criteria!", ]})
        if data['questions'].exists() and len(data['questions']) != data['question_count']:
            raise ValidationError(
                {'questions': ["Questions Selected must be same as Question Count.", ]})
        elif data['question_selection'] != '':
            sel_criteria = data['question_selection']
            que_count = data['question_count']
            exam_obj = super(CreateExamForm, self).save(commit=False)
            rand_ids = []
            if sel_criteria == 'RT' or sel_criteria == 'RUT':
                if not data['topic'].exists():
                    raise ValidationError(
                        {'topic': ["Topics must be selected for Selected Criteria", ]})
                elif sel_criteria == 'RT':
                    # Random Selection From Selected Topic
                    print("RT")
                    # print(topics)
                    topics = data['topic']
                    print(topics)
                    ids = list(Question.objects.values_list(
                        'id', flat=True).filter(topic__in=topics))
                    print(ids)
                    if que_count > len(ids):
                        raise ValidationError(
                            {'question_count': ["Question Count {} is bigger than available questions {} for given Selected Criteria".format(que_count, len(ids)), ]})
                    rand_ids = random.sample(ids, que_count)
                else:
                    # Random Selection From Unused Questions From Selected Topic
                    print("RUT")
                    exams = Exam.objects.all()
                    print(exams)
                    topics = data['topic']
                    print(topics)
                    unused_ids = list(Question.objects.exclude(exam__in=exams).values_list(
                        'id', flat=True).filter(topic__in=topics))
                    print(unused_ids)
                    if que_count > len(unused_ids):
                        raise ValidationError(
                            {'question_count': ["Question Count {} is bigger than available questions {} for given Selected Criteria".format(que_count, len(unused_ids)), ]})
                    rand_ids = random.sample(unused_ids, que_count)
                    print(rand_ids)
            elif sel_criteria == 'R':
                # Random Selection From All
                print("R")
                ids = list(Question.objects.values_list('id', flat=True))
                # print(ids)
                if que_count > len(ids):
                    raise ValidationError(
                        {'question_count': ["Question Count {} is bigger than available questions {} for given Selected Criteria".format(que_count, len(ids)), ]})
                rand_ids = random.sample(ids, que_count)
            elif sel_criteria == 'RU':
                # Random Selection From Unused Questions
                print("RU")
                exams = Exam.objects.all()
                # print(exams)
                unused_ids = list(Question.objects.exclude(
                    exam__in=exams).values_list('id', flat=True))
                # print(unused_ids)
                if que_count > len(unused_ids):
                    raise ValidationError(
                        {'question_count': ["Question Count {} is bigger than available questions {} for given Selected Criteria".format(que_count, len(unused_ids)), ]})
                rand_ids = random.sample(unused_ids, que_count)
            self.cleaned_data['questions'] = Question.objects.filter(
                id__in=rand_ids)
        return super(CreateExamForm, self).save(commit=commit)
