from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)