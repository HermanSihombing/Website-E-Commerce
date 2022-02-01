from django import forms

JLH_PRODUCT = [(i, str(i)) for i in range(1, 10)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=JLH_PRODUCT, coerce=int)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)