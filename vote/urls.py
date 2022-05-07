"""vote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from cik import views as cik
from main import views as main
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', main.main, name='main'),
    path('auth/', include('django.contrib.auth.urls')),
    path('cikhome/', cik.homeView, name='cikhome'),
    path('addcandidate/', cik.candidateVoteView, name='addcandidate'),
    path('addvote/', cik.voteView, name='addvote'),
    path('admin/', admin.site.urls),
    path('registration/', main.registration, name='registration'),
    path('vote/', main.voteView, name='registration'),
    path('addvotegrade/', cik.voteGradeView, name='addvotegrade'),
    path('addterritory/', cik.territoryView, name='addterritory'),
    path('reports/', cik.reportsView, name='reports'),
    path('candidateslist/', cik.reportCandidateVoteView, name='candidatesreport'),
    path('voteslist/', cik.reportVotes, name='votesreport'),


    # path('vote/', cik.VoteCreateView.as_view(), name="vote_create"),
    # path('select2/', include('django_select2.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
