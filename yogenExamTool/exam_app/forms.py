from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Topic, Question


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
