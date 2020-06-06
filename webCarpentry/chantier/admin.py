from django.contrib import admin
from .models import Chantier, Picture

class PictureInLine(admin.StackedInline):
    model = Picture
    fields = ['is_main', 'picture', 'description']
    extra = 4


class ChantierAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Informations du chantier",    {'fields': ['name', 'description', 'date_of_work']}),
    ]
    inlines = [PictureInLine]


admin.site.register(Chantier, ChantierAdmin)
