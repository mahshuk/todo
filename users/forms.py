from django import forms
from django.contrib.auth.models import User

from tasks.models import ToDo


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password"]

        widgets = {
            "password": forms.widgets.PasswordInput()
        }


class ToDoTask(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['username', 'subject', 'date', 'exam', 'add_mark']  # Adjust fields accordingly