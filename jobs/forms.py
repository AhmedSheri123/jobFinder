from django import forms
from .models import JobsModel


class JobsModelForm(forms.ModelForm):

    class Meta:
        model = JobsModel
        fields = ['job_title', 'monthly_salary', 'cert_type', 'experiences', 'gender', 'age_from', 'age_to', 'about_job']
        widgets = {
            'job_title': forms.TextInput(attrs={'class':'form-control job-desc'}),
            'monthly_salary': forms.TextInput(attrs={'class':'form-control', 'placeholder':'راتب شهري'}),
            'cert_type': forms.Select(attrs={'class':'form-control'}),
            'experiences': forms.Textarea(attrs={'class':'form-control', 'rows':'3'}),
            'gender': forms.Select(attrs={'class':'form-control'}),
            'age_from': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'عمر'}),
            'age_to': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'عمر'}),
            'about_job':forms.Textarea(attrs={'class':'form-control', 'rows':'6'}),
        }