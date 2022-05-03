from django.shortcuts import render

from cik.forms import CandidateForm
from main.forms import VoteForm
from cik.models import voteModel, candidateModel
from main.forms import UserRegistrationForm
from django.http import HttpResponseRedirect, HttpResponse


def main(request):
    return render(request, 'main/main.html')


def registration(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return HttpResponseRedirect('/auth/login/')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/registration.html', {'user_form': user_form})


def voteView(request):
    if request.method == "POST" and "btnvote" in request.POST:
        vote = voteModel.objects.get(id_Vote=int(request.POST.get("Vote")))
        return HttpResponse(votesView(request, vote))
    else:
        return render(request, "view/vote.html", {"form": VoteForm})


def votesView(request, vote):
    if request.method == "POST" and "return" in request.POST:
        return HttpResponse(votesView(request))
    else:
        candidate = candidateModel.objects.filter(votecandidatemodel__id_Vote=vote)
        context = {
            "vote": vote,
            "candidates": candidate
        }
        return render(request, "view/candidates.html", context=context)
