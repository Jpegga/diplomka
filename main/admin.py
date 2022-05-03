from django.contrib import admin
from cik.models import *
from easy_select2 import select2_modelform


admin.site.register(voteModel)
admin.site.register(voteGradeModel)
admin.site.register(territoryModel)
admin.site.register(candidateModel)
admin.site.register(voteCandidateModel)
