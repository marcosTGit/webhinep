# forms.py
from django import forms
from .models import *
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox





# 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}))
    asunto = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu mensaje aquí...', 'rows': 5}))

# 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'title', 'description', 'link']




# 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
class SugerenciaForm(forms.Form):
    captcha = ReCaptchaField(
         widget=ReCaptchaV2Checkbox(
            attrs={
                "data-callback": "CallBackSugerencia"  # acá definís tu callback JS
            }
        )
    )
    
    apellido_nombre = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control  required valid', 'placeholder': 'Apellido y nombre'}))
    telefono = forms.CharField(max_length=100, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'puedes consigar un numero de telefono'}))
    email = forms.EmailField(
        validators=[EmailValidator(message="Ingrese un email válido")],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': ''
        })
    )
    tipo_usuario = forms.ChoiceField(choices=TIPO_USUARIO, widget=forms.Select(attrs={'class': 'form-control required' }))
    tipo_sugerencia = forms.ChoiceField(choices=TIPO_SUGERENCIA, widget=forms.Select(attrs={'class': 'form-control required' }))
    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control required',
            'placeholder': 'Escribe tu mensaje aquí...',
            'rows': 5
        })
    )
    
