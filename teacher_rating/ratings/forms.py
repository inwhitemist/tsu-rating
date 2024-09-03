from django import forms
from .models import Action, Teacher

class ActionForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), label='Преподаватель')

    class Meta:
        model = Action
        fields = ['teacher', 'description', 'points']
