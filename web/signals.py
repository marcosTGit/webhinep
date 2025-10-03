
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Suscriptos, Noticia
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .helpers import *
from datetime import date


@receiver(post_save, sender=Suscriptos)
def send_verification_email(sender, instance, created, **kwargs):
    # 00000000000000000000000000000000000000000000000000000
    # 00000000000000000000000000000000000000000000000000000
    if created:  # Solo ejecuta este código si es un registro nuevo
        # token = get_random_string(length=64)
        # print(instance.token)
        # print(instance.email)
        # instance.token = token
        # instance.save()
        url = contruir_url_absoluta(f"/validar-suscripcion/{instance.token}")

        send_vinculation_email(instance.email, instance.email,{
            'platform_name': 'HINEP.WEB',
            'role': 'Suscripto',
            'expiration_date': '24hs',
            'vinculation_url': url
        })

        # send_mail(
        #     'Confirma tu suscripción',
        #     f'Por favor verifica tu correo haciendo clic en el siguiente enlace: {url}',
        #     'noresponder@hinep.com',
        #     [instance.email],
        #     fail_silently=False,
        # )


@receiver(post_save, sender=Noticia)
def enviar_notificaciones(sender, instance, created, enviar=False,**kwargs):
    # 00000000000000000000000000000000000000000000000000000
    # 00000000000000000000000000000000000000000000000000000
    fecha_actual = date.today().strftime('%Y-%m-%d')
    if created and instance.publicacion_activa:  # activa la variable enviar si es un registro CREADO con el estado publicacion activa
        enviar=True
    if not created and instance.publicacion_activa:  # # activa la variable enviar si es un registro ACTUALIZADO con el estado publicacion activa
        enviar=True
    
    if enviar:
        # token = get_random_string(length=64) # genera un token
        # print(instance)
        # print(instance.token)
        # print(instance.email)
        # instance.token = token
        # instance.save()
        # asunto='Hinep - Boletin Informativo'
        url_noticia = contruir_url_absoluta(f"/noticia/{instance.token}")
        
        suscriptos=Suscriptos.objects.filter(estado=True)
        for suscripto in suscriptos:
            
            url_desvinculacion=contruir_url_absoluta(f"/desvincular-boletin/{suscripto.token}")

            # send_mail(
            #     asunto,  # asunto
            #     mensaje,
            #     'noresponder@hinep.com',
            #     [suscripto.email],
            #     fail_silently=False,
            # )

            send_notification_email('marcossebastiant@gmail.com','mtoledo', {
                'title': instance.titulo,
                'message': instance.copete,
                'date': fecha_actual,
                'url': url_noticia,
                'unvinculation_link': url_desvinculacion,
                'unsubscribe_link': url_desvinculacion
            })            