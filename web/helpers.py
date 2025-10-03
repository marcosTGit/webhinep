import uuid
from django.conf import settings
from django.core.exceptions import ValidationError
import os

def contruir_url_absoluta(path):
    default_host = getattr(settings, "DEFAULT_HOST", "http://127.0.0.1:8000")
    return f"{default_host}{path}"


def unique_image_path(instance, filename):
    ext = filename.split('.')[-1]  # Obtiene la extensión del archivo
    unique_filename = f"{uuid.uuid4().hex}.{ext}"  # Genera un nombre único
    return os.path.join('noticias/imagenes/', unique_filename)


def validar_extension_archivo(value):
    """Valida que el archivo tenga una extensión permitida."""

    ext = os.path.splitext(value.name)[1]  # Obtiene la extensión del archivo
    extensiones_permitidas = ['.doc', '.docx', '.pdf', '.xls', '.xlsx']
    if ext.lower() not in extensiones_permitidas:
        raise ValidationError(f'Extensión no permitida. Solo se permiten {", ".join(extensiones_permitidas)}')

# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

    
def send_html_email(subject, template_name, context, to_emails, from_email=None):
    """
    Envía un email HTML renderizado
    
    Args:
        subject: Asunto del email
        template_name: Nombre del template (ej: 'emails/notification_email.html')
        context: Diccionario con variables para el template
        to_emails: Lista de emails destinatarios
        from_email: Email remitente (opcional)
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL
    
    # Agregar URLs base al contexto
    base_url = getattr(settings, 'SITE_URL', 'DEFAULT_SERVER')
    context.update({
        'vinculation_link': f"{base_url}/vinculation",
        'notifications_link': f"{base_url}/notifications",
        'unvinculation_link': f"{base_url}/unvinculation",
        'unsubscribe_link': f"{base_url}/unsubscribe",
    })
    
    # Renderizar template HTML
    html_content = render_to_string(template_name, context)
    
    # Crear versión de texto plano
    text_content = strip_tags(html_content)
    
    # Crear email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=to_emails
    )
    
    # Adjuntar versión HTML
    email.attach_alternative(html_content, "text/html")
    
    # Enviar email
    return email.send()
 
def send_notification_email(user_email, user_name, notification_data):
    """Envía email de notificación"""
    subject = "Nueva notificación - HINEP.WEB"
    template_name = "web/emails/notificacion.html"
    
    context = {
        'user_name': user_name,
        'subject': subject,
        'notification_title': notification_data.get('title', 'Nueva notificación'),
        'notification_message': notification_data.get('message', ''),
        'notification_date': notification_data.get('date', ''),
    }
    
    send_html_email(
        subject=subject,
        template_name=template_name,
        context=context,
        to_emails=[user_email]
    )
 
def send_vinculation_email(user_email, user_name, vinculation_data):
    """Envía email de vinculación"""
    subject = "Invitación para vincular cuenta - Tu Empresa"
    template_name = "web/emails/vinculacion.html"
    
    context = {
        'user_name': user_name,
        'subject': subject,
        'platform_name': vinculation_data.get('platform_name', 'HINEP.WEB'),
        'user_role': vinculation_data.get('role', 'Usuario'),
        'expiration_date': vinculation_data.get('expiration_date', '24hs'),
        'vinculation_url': vinculation_data.get('vinculation_url', '#'),
    }
    
    send_html_email(
        subject=subject,
        template_name=template_name,
        context=context,
        to_emails=[user_email]
    )