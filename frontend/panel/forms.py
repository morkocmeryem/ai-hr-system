from django import forms
from .models import JobPosting
from .models import UploadedCV

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'department', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
        }
class CVUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedCV
        fields = ['file']