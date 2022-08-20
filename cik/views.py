from django.shortcuts import render, redirect
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
        context = {}
        if request.method == "POST":
            form = CandidateVoteForm(request.POST)
            if form.is_valid():
                return redirect('vote_candidates', vote=form.cleaned_data["Vote"].id_Vote)
            else:
                context["form"] = form
        else:
            context["form"] = CandidateVoteForm

        return render(request, "cik/candidateVote.html", context=context)
    else:
        return render(request, "cik/denied.html")


def candidateView(request, vote):
    if request.user.groups.filter(name='CIK').exists():
        candidate = candidateModel.objects.filter(votecandidatemodel__id_Vote=vote)
        vote = voteModel.objects.get(id_Vote=vote)
        context = {
            "form": CandidateForm,
            "vote": vote,
            "candidates": candidate,
            'id' : idCandidateForm,
        }

        if request.method == "POST":
            if "btnform" in request.POST:
                form = CandidateForm(request.POST, request.FILES)
                if form.is_valid():
                    file = form.cleaned_data["Image"]
                    fs = FileSystemStorage()
                    fs.save(file.name, file)
                    candidate = candidateModel(fio=form.cleaned_data["FIO"], description=form.cleaned_data["Description"], image=form.cleaned_data["Image"])
                    candidate.save()
                    voteCandidateModel(id_Candidate=candidate, id_Vote=vote).save()
                else:
                    context["form"] = form
        elif len(request.GET) > 0:
                del_id = int(request.GET.get("delete", -1))
                change_id = int(request.GET.get("change", -1))

                if del_id != -1:
                    try:
                        candidateModel.objects.get(id_Candidate=del_id).delete()

                    except Exception as e:
                        pass

                    return redirect('vote_candidates', vote=vote.id_Vote)

                if change_id != -1:
                    try:
                        return redirect('candidate_change', vote.id_Vote, change_id)

                    except Exception as e:
                        pass

                    return redirect('vote_candidates', vote=vote.id_Vote)

        return render(request, "cik/candidate.html", context=context)
    else:
        return render(request, "cik/denied.html")


def candidateChangeView(request, vote, id):
    if request.user.groups.filter(name='CIK').exists():
        candidate = candidateModel.objects.get(pk=id)
        data = {
            'FIO': candidate.fio,
            'Description': candidate.description,
            'Image': candidate.image
        }
        form = CandidateForm(initial=data)

        context = {
            'form': form,
            'vote': vote,
            'candidate': candidate
        }

        if request.method == "POST":
            if "change" in request.POST:
                candidate.fio = request.POST.get('FIO')
                candidate.description = request.POST.get('Description')
                try:
                    file = request.FILES['Image']
                    fs = FileSystemStorage()
                    filename = fs.save(file.name, file)
                    candidate.image = file

                except Exception as e:
                    pass

                candidate.save()
                return redirect('vote_candidates', vote=vote)

        else:
            return render(request, 'cik/candidateChange.html', context=context)

    else:
        return render(request, "cik/denied.html")


def voteView(request):
    if request.user.groups.filter(name='CIK').exists():
        form = VoteForm()
        votes = voteModel.objects.all()
        context = {
            "form": form,
            "votes": votes
        }

        if request.method == "POST":
            vote = voteModel()
            grade = voteGradeModel.objects.get(id_Grade=int(request.POST.get("VoteGrade")))
            territory = territoryModel.objects.get(id_Terr=int(request.POST.get("Territory")))
            vote.id_Grade = grade
            vote.id_Terr = territory
            vote.save()
            return redirect("vote_candidates", vote.id_Vote)

        elif len(request.GET) > 0:
                del_id = int(request.GET.get("delete", -1))
                change_id = int(request.GET.get("change", -1))

                if del_id != -1:
                    try:
                        voteModel.objects.get(id_Vote=del_id).delete()

                    except Exception as e:
                        pass

                    return redirect('addvote')

                if change_id != -1:
                    try:
                        return redirect('vote_change', change_id)

                    except Exception as e:
                        pass

                    return redirect('addvote')

        return render(request, "cik/vote.html", context=context)
    else:
        return render(request, "cik/denied.html")


def voteChangeView(request, id):
    if request.user.groups.filter(name='CIK').exists():
        vote = voteModel.objects.get(pk=id)
        data = {
            'VoteGrade': vote.id_Grade,
            'Territory': vote.id_Terr,
        }
        form = VoteForm(initial=data)

        if request.method == "POST":
            if "change" in request.POST:
                vote.id_Grade = voteGradeModel.objects.get(id_Grade=int(request.POST.get("VoteGrade")))
                vote.id_Terr = territoryModel.objects.get(id_Terr=int(request.POST.get("Territory")))
                vote.save()
                return redirect('addvote')

        return render(request, 'cik/voteChange.html', {'form': form})

    else:
        return render(request, "cik/denied.html")


def voteGradeView(request):
    if request.user.groups.filter(name='CIK').exists():
        model = voteGradeModel.objects.all()
        context = {"form": VoteGradeForm,
                   "model": model}

        if request.method == "POST":
            voteGrade = voteGradeModel()
            voteGrade.grade = request.POST.get("grade")
            voteGrade.name = request.POST.get("name")
            voteGrade.save()
            return redirect('addvotegrade')

        elif len(request.GET) > 0:
                del_id = int(request.GET.get("delete", -1))
                change_id = int(request.GET.get("change", -1))

                if del_id != -1:
                    try:
                        voteGradeModel.objects.get(id_Grade=del_id).delete()

                    except Exception as e:
                        pass

                    return redirect('addvotegrade')

                if change_id != -1:
                    try:
                        return redirect('votegrade_change', change_id)

                    except Exception as e:
                        pass

                    return redirect('addvotegrade')

        return render(request, "cik/votegrade.html", context=context)
    else:
        return render(request, "cik/denied.html")


def voteGradeChange(request, id):
    if request.user.groups.filter(name='CIK').exists():
        votegrade = voteGradeModel.objects.get(pk=id)
        data = {
            'grade': votegrade.grade,
            'name': votegrade.name,
        }
        form = VoteGradeForm(initial=data)

        if request.method == "POST":
            if "change" in request.POST:
                votegrade.grade = request.POST.get('grade')
                votegrade.name = request.POST.get('name')
                votegrade.save()
                return redirect('addvotegrade')

        return render(request, 'cik/voteGradeChange.html', {'form': form})

    else:
        return render(request, "cik/denied.html")


def territoryView(request):
    if request.user.groups.filter(name='CIK').exists():
        model = territoryModel.objects.all()
        context = {"form": TerritoryForm,
                   "model": model}

        if request.method == "POST":
            territory = territoryModel()
            territory.id_Grade = voteGradeModel.objects.get(id_Grade=int(request.POST.get("voteGrade")))
            territory.territory_Name = request.POST.get("name")
            territory.save()
            return redirect('addterritory')

        elif len(request.GET) > 0:
                del_id = int(request.GET.get("delete", -1))
                change_id = int(request.GET.get("change", -1))

                if del_id != -1:
                    try:
                        territoryModel.objects.get(id_Terr=del_id).delete()

                    except Exception as e:
                        pass

                    return redirect('addterritory')

                if change_id != -1:
                    try:
                        return redirect('territory_change', change_id)

                    except Exception as e:
                        pass

                    return redirect('addterritory')

        return render(request, "cik/territory.html", context=context)
    else:
        return render(request, "cik/denied.html")


def territoryChangeView(request, id):
    if request.user.groups.filter(name='CIK').exists():
        territory = territoryModel.objects.get(pk=id)
        data = {
            'voteGrade': territory.id_Grade,
            'name': territory.territory_Name,
        }
        form = TerritoryForm(initial=data)

        if request.method == "POST":
            if "change" in request.POST:
                territory.id_Grade = voteGradeModel.objects.get(id_Grade=int(request.POST.get("voteGrade")))
                territory.territory_Name = request.POST.get('name')
                territory.save()
                return redirect('addterritory')

        return render(request, 'cik/territoryChange.html', {'form': form})

    else:
        return render(request, "cik/denied.html")


def reportsView(request):
    if request.user.groups.filter(name='CIK').exists():
        return render(request, "cik/reports.html")
    else:
        return render(request, "cik/denied.html")


def reportCandidateVoteView(request):
    if request.user.groups.filter(name='CIK').exists():
        if request.method == "POST":
            vote = voteModel.objects.get(id_Vote=int(request.POST.get("Vote")))
            return redirect('candidates_report', vote.id_Vote)

        else:
            return render(request, "cik/candidateVote.html", {"form": CandidateVoteForm})

    else:
        return render(request, "cik/denied.html")


def reportCandidateView(request, id):
    if request.user.groups.filter(name='CIK').exists():
        candidate = candidateModel.objects.filter(votecandidatemodel__id_Vote=id)
        vote = voteModel.objects.get(pk=id)
        context = {
            "vote": vote,
            "candidates": candidate
        }
        return render(request, "cik/candidatesreport.html", context=context)

    else:
        return render(request, "cik/denied.html")


def reportVotes(request):
    if request.user.groups.filter(name='CIK').exists():
        votes = voteModel.objects.all()
        return render(request, 'cik/votesreport.html', {'votes': votes})

    else:
        return render(request, 'cik/denied.hmtl')
