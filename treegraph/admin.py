from django.contrib import admin

from .models import *


class EdgesInline(admin.StackedInline):
    model = Edges
    fk_name = 'child'

    fieldsets = [
        ('Связь', {'fields': ['parent']}),
    ]


class LevelInline(admin.StackedInline):
    model = Levels
    extra = Nodes.objects.count()

    fieldsets = [
        ('Связь', {'fields': ['node_id', 'level']}),
    ]


class GraphAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Понятие', {'fields': ('name', 'lvl')}),
    )

    inlines = [EdgesInline]
    list_display = ('name', 'lvl')
    list_filter = ['lvl']
    search_fields = ['name']


class StudentsAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Студент', {'fields': ('group', 'first_name', 'last_name')}),
    )

    inlines = [LevelInline]
    list_display = ('group', 'first_name', 'last_name')


admin.site.register(Nodes, GraphAdmin)
# admin.site.register(Edges)
admin.site.register(TimeSettings)
# admin.site.register(Levels)
admin.site.register(Students, StudentsAdmin)



