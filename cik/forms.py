import django_select2.forms
from django import forms
import cik.models
from cik.models import *
import easy_select2
from django_select2 import forms as s2forms


class CandidateVoteForm(forms.Form):
    Vote = forms.ModelChoiceField(label="Выборы", queryset=voteModel.objects.all())


class CandidateForm(forms.Form):
    FIO = forms.CharField(label="ФИО кандидата", min_length=10, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Иванов Иван Иванович'}))
    Description = forms.CharField(label="Описание", widget=forms.Textarea(attrs={'placeholder': 'Описание'}))
    Image = forms.ImageField(label="Фотография кандидата")



class VoteForm(forms.Form):
    VoteGrade = forms.ModelChoiceField(label="Уровень выборов", queryset=voteGradeModel.objects.all())
    Territory = forms.ModelChoiceField(label="Территория", queryset=territoryModel.objects.all())


# class VoteWidget(easy_select2.Select2Mixin):
#     search_fields = [
#         "username__icontains",
#         "email__icontains",
#     ]
#
#
# class VoteForm(forms.ModelForm):
#     class Meta:
#         model = vote
#         fields = "__all__"
#         widgets = {
#             "vote": VoteWidget,
#         }


# class VoteWidget(forms.Form):
#     voteGrade = forms.ModelChoiceField(
#         queryset=vote_Grade.objects.all(),
#         label=u"Уровень выборов",
#         widget=s2forms.ModelSelect2Widget(
#             model=vote_Grade,
#             search_fields=['name__icontains'],
#         )
#     )
#
#     terr = forms.ModelChoiceField(
#         queryset=territory.objects.all(),
#         label=u"Территория проведения выборов",
#         widget=s2forms.ModelSelect2Widget(
#             model=territory,
#             fields=("territory_Name", ),
#             search_fields=['name__icontains'],
#             dependent_fields={'vote_Grade': 'id_Grade'},
#             max_results=100,
#         )
#     )
#
#
# class VoteForm(forms.ModelForm):
#     class Meta:
#         model = vote_Grade
#         fields = ("grade", )
#         widgets = {
#             "grade": s2forms.Select2Widget,
#         }
