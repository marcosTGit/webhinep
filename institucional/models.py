

import os
from django import forms
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator, MinLengthValidator, EmailValidator
from django.utils import timezone
from web.constantes import *
from web.helpers import *
from django.contrib.auth.models import User
from private_storage.fields import PrivateFileField


import uuid

# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

class PersonalHospital(models.Model):
    numero_agente= models.BigIntegerField( default=0)  # Un campo para identificar el registro
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Correo electrónico no válido")],
        null=True,
        blank=True
    )
    estado = models.BooleanField(default=False)
    email_validado = models.BooleanField(default=False)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    registro_creado = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    # Fecha y hora cada vez que se actualiza
    registro_actualizado = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )
    def __str__(self):
        return f"{self.email}"
    
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

class Articulo(models.Model):
    #definimos la fecha en la que comenzara la publicacion 
    fecha_publicacion = models.DateField(
        verbose_name="fecha de publicacion",
        default=timezone.now,
    )
    
    tipo_documento = models.CharField(max_length=30, choices=TIPO_DOCUMENTO, default='', null=True)    
    titulo = models.CharField(max_length=200, blank=False)  # Título
    subtitulo = models.CharField(max_length=200, null=True, blank=True)  # titulo del contenido destacado 
    contenido = models.TextField(blank=False)  # contenido 
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='autor', editable=False, null=True, blank=True)  # Relación con el usuario
    # archivo = models.FileField(
    #     upload_to='Articulos/',
    #     validators=[validar_extension_archivo],  # Aplica la validación de extensión
    #     blank=True,  # Permite que el campo sea opcional
    #     null=True
    # )
    registro_creado = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )
    # Fecha y hora cada vez que se actualiza
    registro_actualizado = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    def __str__(self):
        return f'{self.fecha_publicacion} {self.titulo}' or "No hay articulos"
    
    def save(self, *args, **kwargs):
        # Convertir el título y contenido a mayúsculas antes de guardar
        if self.titulo:
            self.titulo = self.titulo.upper()
        if self.subtitulo:
            self.subtitulo = self.subtitulo.upper()
        
        super().save(*args, **kwargs)  # Llamar al método original de Django

        # Guarda la nueva imagen

    
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # Obtiene la extensión
    valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx', '.xls', '.xlsx']
    
    if not ext.lower() in valid_extensions:
        raise ValidationError('Tipo de archivo no permitido. Formatos aceptados: ' + ', '.join(valid_extensions))


class FileArticulo(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='imagenes')
    # imagen = models.ImageField(upload_to=unique_image_path)
    archivo_restringido = PrivateFileField(
        'documento', 
        blank=True,
        null=True,
        validators=[validate_file_extension],  # ← Validador personalizado
        content_types=[
            'application/pdf',
            'image/jpeg', 
            'image/png',
            'application/msword',  # .doc
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # .docx
            'application/vnd.ms-excel',  # .xls
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # .xlsx
        ],
        max_file_size=1024 * 1024 * 10,  # 10MB
    )  # Se guardará en MEDIA_ROOT/documentos/
    
    archivo_publico = models.FileField(upload_to='documentos/', blank=True, null=True)  # Se guardará en MEDIA_ROOT/documentos/
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"File de {self.articulo.titulo}"
    
    def get_queryset(self):
        # Make sure only certain objects can be accessed.
        return super().get_queryset().filter(...)

    def can_access_file(self, private_file):
        # When the object can be accessed, the file may be downloaded.
        # This overrides PRIVATE_STORAGE_AUTH_FUNCTION
        # return True    
        user = self.user
        print("00000000000000000000000000000000000000000000000000000000000")    
        # 1. El dueño siempre puede acceder
        if private_file.owner == user:
            return True        
    
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

# class ImagenArticulo(models.Model):
#     articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='imagenes')
#     imagen = models.ImageField(upload_to=unique_image_path)
#     descripcion = models.CharField(max_length=255, blank=True, null=True)

#     def __str__(self):
#         return f"imagen de {self.articulo.titulo}"