

import os
from django import forms
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator, MinLengthValidator, EmailValidator
from django.utils import timezone
from web.constantes import *
import uuid

# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

# Create your models here.
class Slider(models.Model):
    image = models.ImageField(upload_to='slider/')  # Ruta donde se almacenarán las imágenes
    titulo = models.CharField(max_length=100, blank=True)  # Título de la imagen
    titulo_color = models.CharField(max_length=30, choices=COLORES, default='', null=True, blank=True)    
    subtitulo = models.TextField(blank=True)  # Descripción de la imagen
    link = models.URLField(blank=True)  # Enlace opcional
    link_texto = models.CharField(max_length=100, blank=True)  # Título de la imagen
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Fecha de subida automática
    #definimos la fecha en la que comenzara la publicacion 
    fecha_publicacion = models.DateField(
        verbose_name="fecha de publicacion",
        default=timezone.now,
    )
    #definimos la fecha en la que caduca la publicacion 
    fin_publicacion = models.DateField(
        verbose_name="Fin de publicacion",
        default=None,
        blank=True,
        null=True
    )
    publicacion_activa = models.BooleanField(default=False)    

    def __str__(self):
        return self.titulo or "Imagen sin título"


# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='galeria/')  # Ruta donde se almacenarán las imágenes
    title = models.CharField(max_length=100, blank=True)  # Título de la imagen
    description = models.TextField(blank=True)  # Descripción de la imagen
    link = models.URLField(blank=True)  # Enlace opcional
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Fecha de subida automática

    def __str__(self):
        return self.title or "Imagen sin título"

    def save(self, *args, **kwargs):
        # Verifica si existe un registro con esta instancia y si tiene una imagen previa
        if self.pk:
            imagen_anterior = Image.objects.filter(pk=self.pk).first()
            if imagen_anterior and imagen_anterior.image != self.image:
                if imagen_anterior.image:
                    if os.path.isfile(imagen_anterior.image.path):
                        os.remove(imagen_anterior.image.path)

        # Guarda la nueva imagen
        super().save(*args, **kwargs)

# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

class Suscriptos(models.Model):
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Correo electrónico no válido")]
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    estado = models.BooleanField(default=False)
    registro_creado = models.DateTimeField(
        auto_now_add=True,  # Fecha y hora al momento de crear
        verbose_name="Fecha de creación"
    )
    registro_actualizado = models.DateTimeField(
        auto_now=True,  # Fecha y hora cada vez que se actualiza
        verbose_name="Última actualización"
    )
    def __str__(self):
        return self.email or "No hay suscriptos"
    



# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

# Create your models here.
class Noticia(models.Model):
    #definimos la fecha en la que comenzara la publicacion 
    fecha_publicacion = models.DateField(
        verbose_name="fecha de publicacion",
        default=timezone.now,
    )
    #definimos la fecha en la que caduca la publicacion 
    fin_publicacion = models.DateField(
        verbose_name="Fin de publicacion",
        default=None,
        blank=True,
        null=True
    )
    publicacion_activa = models.BooleanField(default=False)
    enviar_boletin = models.BooleanField(default=False)
    titulo = models.CharField(max_length=200, blank=False)  # Título
    copete = models.CharField(max_length=200, blank=True)  # Subtitulo o copete
    contenido = models.TextField(blank=False)  # contenido 
    imagen = models.ImageField(upload_to='noticias/', blank=True, null=True)  # Ruta donde se almacenarán las imágenes
    ajustar_imagen = models.IntegerField(
        default=100, 
        null=False,
        validators=[
            MinValueValidator(0),  # mínimo 0
            MaxValueValidator(100)  # máximo 100
        ]
        )
    epigrafe = models.TextField(blank=True)  # Descripción de la imagen
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    titulo_destacado = models.CharField(max_length=200, null=True, blank=True)  # titulo del contenido destacado 
    contenido_destacado = models.TextField(null=True, blank=True)  # Contenido destacado 
    estilo_destacado = models.CharField(max_length=30, choices=COLORES, default='', null=True)    
    # Fecha y hora al momento de crear
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
        return f'{self.fecha_publicacion} {self.titulo}' or "No hay noticias para mostrar"
    


    #     super().save(*args, **kwargs)
    

# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

class Configuracion(models.Model):
    nombre = models.CharField(max_length=100)  # Un campo para identificar el registro
    data = models.JSONField(max_length=200, null=True, blank=True)  # titulo del contenido destacado 
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
        return self.nombre
    

# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# AQUI PODRIAMOS DEFINIR VARIABLES COMO NUMERO DE TELEFONOS
class Sugerencia(models.Model):
    apellido_nombre = models.CharField(max_length=200, default="", blank=True, null=True )  # Un campo para identificar el registro
    telefono = models.CharField(max_length=15, default="", blank=True, null=True)  # Un campo para identificar el registro
    email = models.EmailField(
        # unique=True,
        default="",
        blank=True,
        null=True,
        validators=[EmailValidator(message="Correo electrónico no válido")]
    )
    tipo_usuario = models.CharField(max_length=100) # titulo del contenido destacado null
    tipo_sugerencia = models.CharField(max_length=100) # titulo del contenido destacado 
    mensaje = models.TextField(blank=False, default="", null=False)  # contenido 
    
    registro_creado = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    # Fecha y hora cada vez que se actualiza
    # registro_actualizado = models.DateTimeField(
    #     auto_now=True,
    #     verbose_name="Última actualización"
    # )
    def __str__(self):
        return f"{self.apellido_nombre} {self.tipo_sugerencia}"

# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

class PersonalHospital(models.Model):
    numero_agente= models.IntegerField( default=0)  # Un campo para identificar el registro
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Correo electrónico no válido")],
        null=True,
        blank=True
    )
    estado = models.BooleanField(default=False)
    email_validado = models.BooleanField(default=False)
    nombre = models.CharField(max_length=100)  # Un campo para identificar el registro
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
        return self.numero_agente