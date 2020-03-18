#arquivo forms.py
from django import forms
from django.contrib.auth.models import User
user = User()

class MeuForm(forms.Form):
     Funcionarios = forms.ChoiceField(choices=[('0', '--Selecione--')]+ [(user.id, user.username) for user in User.objects.all()])
