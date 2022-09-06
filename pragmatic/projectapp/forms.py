from django.forms import ModelForm
from .models import Project


class ProjectCreationForm(ModelForm):
    class Meta:
        model=Project
        fields = ['title','des','image']