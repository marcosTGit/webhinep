# forms.py
from django import forms
# from .models import Image

# class ContactoForm(forms.Form):
#     nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}))
#     asunto = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto'}))
#     mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu mensaje aquí...', 'rows': 5}))


# class ImageForm(forms.ModelForm):
#     class Meta:
#         model = Image
#         fields = ['image', 'title', 'description', 'link']
