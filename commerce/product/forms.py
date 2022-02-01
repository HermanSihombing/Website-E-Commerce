from django import forms
from .models import Reviewed

class ReviewedForm(forms.ModelForm):
    class Meta:
        model = Reviewed
        fields = ('comment',)