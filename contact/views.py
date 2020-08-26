from django.shortcuts import render
from .models import Contact
from .forms import ContactForm
from django.views.generic import CreateView

# Create your views here.

class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = '/'
