from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1')
        model = get_user_model()
