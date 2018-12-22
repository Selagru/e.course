from django import forms

from .models import *


class NodeForm(forms.ModelForm):

    class Meta:
        model = Nodes
        fields = ('name', 'lvl')
