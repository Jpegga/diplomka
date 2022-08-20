from django import forms
import cik.models
from cik.models import *


class CandidateVoteForm(forms.Form):
    Vote = forms.ModelChoiceField(label="Выборы", queryset=voteModel.objects.all())


class CandidateForm(forms.Form):
    FIO = forms.CharField(label="ФИО кандидата", min_length=10, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Иванов Иван Иванович'}))
    Description = forms.CharField(label="Описание", widget=forms.Textarea(attrs={'placeholder': 'Описание'}))
    Image = forms.ImageField(label="Фотография кандидата")


class idCandidateForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput())


class VoteForm(forms.Form):
    VoteGrade = forms.ModelChoiceField(label="Уровень выборов", queryset=voteGradeModel.objects.all())
    Territory = forms.ModelChoiceField(label="Территория", queryset=territoryModel.objects.all())


class VoteGradeForm(forms.Form):
    grade = forms.FloatField(label="Уровень", min_value=1, max_value=3, widget=forms.NumberInput(attrs={'placeholder': 'Число'}))
    name = forms.CharField(label="Название")


class TerritoryForm(forms.Form):
    voteGrade = forms.ModelChoiceField(label="Уровень выборов", queryset=voteGradeModel.objects.all())
    name = forms.CharField(label="Название территории")
