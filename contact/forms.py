from django import forms
from .models import Contact
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class ContactForm(forms.ModelForm):
    recaptcha = ReCaptchaField()

    class Meta:
        model = Contact
        fields = ('email', 'recaptcha')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'editContent', 'placeholder': 'Введите емейл...'})
        }
        labels = {
            'email': '',
        }