from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from blogs.models import Profile

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_picture', 'bio', 'github', 'linkedin', 'website')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }