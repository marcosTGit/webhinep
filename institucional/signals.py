
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import PersonalHospital
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from web.helpers import *

@receiver(pre_save, sender=PersonalHospital)
def send_verification_email(sender, instance, **kwargs):
    # 00000000000000000000000000000000000000000000000000000
    # 00000000000000000000000000000000000000000000000000000
    if instance.pk:  # Solo ejecutar si ya existe (es una actualización)
        old_instance = sender.objects.get(pk=instance.pk)  # Obtener valores antiguos    

        if old_instance.email != instance.email and instance.email:  # Si el email cambió y no es nulo
            url = contruir_url_absoluta(f"/validar-usuario-institucional/{instance.token}")
            # send_mail(
            #     'Hinep Correo - Usuario HINEP',
            #     f'Por favor verifica tu correo haciendo clic en el siguiente enlace: {url}',
            #     'noresponder@hinep.com',
            #     [instance.email],
            #     fail_silently=False,
            # )

            send_vinculation_email(instance.email, instance.email,{
                'platform_name': 'HINEP.WEB',
                'role': 'usuario_institucional',
                'expiration_date': '24hs',
                'vinculation_url': url
            })
  

