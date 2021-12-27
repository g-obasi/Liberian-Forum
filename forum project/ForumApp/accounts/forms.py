from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


# form to create a new user (i.e sign up from) the user profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=200, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


# form to update the user profile
class UserInfoUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'date_of_birth', 'gender', 'profile_pic', 'bio', 'location')
        widgets = {'date-of_birth': forms.DateInput(attrs={'type': 'date'})}
