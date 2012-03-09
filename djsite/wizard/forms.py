# Create your forms here.
from django import forms
from django.forms import ModelForm
from models import Project
import djos

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('title','date_created', 'path')
        
    def clean_path(self):
        p = self.cleaned_data.get('path', '')
        t = self.cleaned_data.get('title', '')
        valid = djos.create_project_dirs(self.cleaned_data)
        if not valid:
            raise forms.ValidationError("I could not create this path: %s. Please check the path and try different one." % (p))
        return p