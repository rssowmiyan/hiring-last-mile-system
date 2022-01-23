from statistics import mode
from django import forms
from django.db import models
from django.db.models import fields
from .models import Sequence,Funnel,DefaultTemplates

class FunnelForm(forms.ModelForm):
    class Meta:
        model = Funnel
        fields = ['funnel_name','segment','sub_segment']

class SequenceForm(forms.ModelForm):
    # sequence = forms.ModelMultipleChoiceField(queryset=DefaultTemplates.objects.all(),initial=0)
    class Meta:
        model = Sequence
        fields = ['sequence_name','description','frequency','sequence']
    def __init__(self, *args, **kwargs):
        super(SequenceForm, self).__init__(*args, **kwargs)
        self.fields['sequence'].empty_label = "Choose a template"


class DefaultTemplatesForm(forms.ModelForm):
    class Meta:
        model = DefaultTemplates
        fields = '__all__'