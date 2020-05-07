from django import forms

from apps.contact import models


class ContactForm(forms.ModelForm):
    class Meta:
        model = models.Contact
        fields = ['name', 'email', 'message']
