from django import forms
from django.contrib.auth.models import User
from cik.models import voteModel


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class VoteForm(forms.Form):
    Vote = forms.ModelChoiceField(label="Выборы", queryset=voteModel.objects.all())
