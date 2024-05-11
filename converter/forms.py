# forms.py
from django import forms

class VTTUploadForm(forms.Form):
    vtt_file = forms.FileField()
