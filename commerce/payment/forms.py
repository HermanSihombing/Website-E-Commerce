from django import forms

class PaymentForm(forms.Form):
    nama_lengkap = forms.CharField(label="Nama Lengkap", widget=forms.TextInput(attrs={'placeholder': 'Masukkan Nama Lengkap'}))
    phone = forms.CharField(label="No HP", widget=forms.TextInput(attrs={'placeholder': 'Masukkan Handphone'}))
    email = forms.CharField(label="Masukkan Email", widget=forms.TextInput(attrs={'placeholder': 'Masukkan Email'}))
    catatan = forms.CharField(label="Masukkan catatan", widget=forms.TextInput(attrs={'placeholder': 'Masukkan catatan'}))