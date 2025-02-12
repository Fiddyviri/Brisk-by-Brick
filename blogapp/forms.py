from django import forms

class NewsletterForm(forms.Form):
    first_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField( max_length=15, required=False)