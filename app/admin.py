from django.contrib import admin
from . import models
# Register your models here.=
admin.site.register(models.User)
admin.site.register(models.VotingM)
admin.site.register(models.SelectionKing)
admin.site.register(models.SelectionQueen)
admin.site.register(models.SelectionImageKing)
admin.site.register(models.SelectionImageQueen)
admin.site.register(models.Device)

admin.site.register(models.FinishKingGroup)
admin.site.register(models.FinishQueenGroup)