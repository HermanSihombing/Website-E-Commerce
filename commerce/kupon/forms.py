from django import forms

class KuponApplyForm(forms.Form):
    code = forms.CharField()