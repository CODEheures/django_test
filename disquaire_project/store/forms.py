from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Nom',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )