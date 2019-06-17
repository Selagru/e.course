from django.contrib import admin

from .models import *


class EdgesInline(admin.StackedInline):
    model = Edges
    fk_name = 'child'

    fieldsets = [
        ('Связь', {'fields': ['parent']}),
    ]


class GraphAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Понятие', {'fields': ('name', 'lvl')}),
    )

    inlines = [EdgesInline]
    list_display = ('name', 'lvl', 'depth')
    list_filter = ['depth']
    search_fields = ['name', 'lvl']


admin.site.register(Nodes, GraphAdmin)
admin.site.register(Edges)
admin.site.register(TimeSettings)



