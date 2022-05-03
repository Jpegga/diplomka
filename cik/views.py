from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from cik.forms import *
from django.views import generic, View
from cik.models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied


def homeView(request):
    if request.user.groups.filter(name='CIK').exists():
        return render(request, "cik/CIK.html")
    else:
        return render(request, "cik/denied.html")


def candidateVoteView(request):
    if request.user.groups.filter(name='CIK').exists():
        if request.method == "POST" and "btnvote" in request.POST:
            vote = voteModel.objects.get(id_Vote=int(request.POST.get("Vote")))
            return HttpResponse(candidateView(request, vote))
        else:
            return render(request, "cik/candidateVote.html", {"form": CandidateVoteForm})
    else:
        return render(request, "cik/denied.html")


def candidateView(request, vote):
    if request.user.groups.filter(name='CIK').exists():
        if request.method == "POST" and "btnform" in request.POST:
            candidate = candidateModel()
            candidate.fio = request.POST.get("FIO")
            candidate.description = request.POST.get("Description")
            file = request.FILES["Image"]
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            candidate.image = file
            candidate.save()
            voteCandidate = voteCandidateModel()
            voteCandidate.id_Vote = voteModel.objects.get(id_Vote=int(request.POST.get("Vote")))
            voteCandidate.id_Candidate = candidateModel.objects.get(id_Candidate=int(candidate.id_Candidate))
            voteCandidate.save()
            return HttpResponseRedirect('/addcandidate/')
        elif request.method == "POST" and "btnreturn" in request.POST:
            return HttpResponse(candidateView(request))
        else:
            candidate = candidateModel.objects.filter(votecandidatemodel__id_Vote=vote)
            context = {
                "form": CandidateForm,
                "vote": vote,
                "candidates": candidate
            }
            return render(request, "cik/candidate.html", context=context)
    else:
        return render(request, "cik/denied.html")


def voteView(request):
    if request.user.groups.filter(name='CIK').exists():
        if request.method == "POST":
            vote = voteModel()
            grade = voteGradeModel.objects.get(id_Grade=int(request.POST.get("VoteGrade")))
            territory = territoryModel.objects.get(id_Terr=int(request.POST.get("Territory")))
            vote.id_Grade = grade
            vote.id_Terr = territory
            vote.save()
            return HttpResponseRedirect("/addcandidate/")
        votefor = VoteForm()
        votes = voteModel.objects.all()
        voteCandidate = voteCandidateModel()
        context = {"form": votefor,
                   "votes": votes,
                   "voteCandidate": voteCandidate}
        return render(request, "cik/vote.html", context=context)
    else:
        return render(request, "cik/denied.html")

# class VoteCreateView(generic.CreateView):
#     model = vote_Grade
#     form_class = VoteWidget()
#     success_url = "vote/"
#     def get(self, request):
#         return render(request, 'cik/vote.html', {"form": VoteWidget()})