from django.views.generic.edit import FormView

from apps.contact import forms


class ContactView(FormView):
    template_name = 'contact/contact.html'
    form_class = forms.ContactForm
    success_url = '/thanks/'
