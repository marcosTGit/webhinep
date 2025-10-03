import json
from django.contrib import messages  # importamos lo smensajes flash 
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import * # Image, Suscriptos, Noticia # imprtamos los modelos
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
# from .forms import ContactoForm, ImageForm  # importamos lo sformularios 
# from .api_get import getMenuPortalAPi, getContenidoURL
import re
import uuid
from django.utils.safestring import mark_safe
from django.utils.timezone import now

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from web.helpers import *

# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # DSECARGA O ACCESO RESTRINGOIOD SOLO PARA USARIO LOGEADOS

from private_storage.views import PrivateStorageDetailView
# # from .models import Document
from private_storage.views import PrivateStorageDetailView
class MyStorageView(PrivateStorageDetailView):
    print("####################################################################################")    
    print("####################################################################################")    
    print("####################################################################################")    
    print("####################################################################################")    
    model = FileArticulo
    model_file_field = 'archivo_restringido'
    
    def get_queryset(self):
        # Make sure only certain objects can be accessed.
        return super().get_queryset().filter(...)

    def dispatch(self, request, *args, **kwargs):
        print("=== DISPATCH llamado ===")
        print(f"Usuario: {request.user}")
        print(f"URL: {request.path}")
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        print("=== GET_OBJECT llamado ===")
        obj = super().get_object(queryset)
        print(f"Objeto: {obj}")
        print(f"Owner del objeto: {obj.owner}")
        return obj
    
    def can_access_file(self, private_file):
        print("=== CAN_ACCESS_FILE llamado ===")
        print(f"Private file: {private_file}")
        print(f"Usuario: {self.request.user}")
        print(f"Owner del file: {private_file.owner}")

    # 00000000000000000000000000000000000000000000000000000000000000000000000000
    # 00000000000000000000000000000000000000000000000000000000000000000000000000

    def can_access_file(self, private_file):
        # Solo el dueño puede acceder
        # return private_file.owner == self.request.user
        user = self.request.user
        print("00000000000000000000000000000000000000000000000000000000000")    
        # 1. El dueño siempre puede acceder
        if private_file.owner == user:
            return True
            
        # # 2. Los administradores pueden acceder (ya funciona)
        # if user.is_staff:
        #     return True
        # else:
        #     print("No es admin")                
        # # 3. Agregar aquí otras condiciones según tu necesidad:
         
        # # Ejemplo: Usuarios en mismo grupo/departamento
        # if user.groups.filter(name='usuario_institucional').exists():
        #     return True
        # else:
        #     print("no pretenece al grupo intitucionl")
         
        # # Ejemplo: Usuarios con un permiso específico
        # # if user.has_perm('mi_app.puede_ver_documentos'):
        # #     return True
            
        # # Ejemplo: Usuarios específicos por nombre
        # if user.username in ['usuario1', 'prueba']:
        #     return True
        # else:
        #     print("no esta enla lista permitica")
            
        return False    
    

# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

# def login_institucional(request):
#     return render(request, 'institucional/login_institucional.html')


# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# @csrf_exempt  # Usar solo si estás haciendo pruebas. Mejor usar csrf_token en el template.
def RegistrarUsuario(request):
    try:
        datos=json.loads(request.body)
        if request.method == 'POST' and datos['email'] and datos['numero_agente_cuil'] and datos['token']: # los datos estan 
            # ahora intentamos almancendar en la base de datos con validacion incluida
            try:
                validate_email(datos['email'])
            except ValidationError:
                return JsonResponse({"error": "El formato del email no es válido."}, status=400)

            try:
                empleado_hospital = PersonalHospital.objects.get(numero_agente = datos['numero_agente_cuil'])
                empleado_hospital.email=datos['email']
                empleado_hospital.save()
                return JsonResponse({"mensaje": "Registro exitoso. revisa tu casilla de correo"}, status=201)
            except:
                return JsonResponse({"error": "Personal no registrado"}, status=400)

        else:
            # faltan parametros 
            return JsonResponse({"error": "datos incorrectos"}, status=400)
            # return JsonResponse({'message': 'me esta falatndo algo'})
    except:
        return JsonResponse({'error': 'Metodo no permitido'}, status=405)
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

def ValidarRegistro(request, token):

    # Obtener el registro específico
    try:
        empleado_hospital = PersonalHospital.objects.get(token=token)
        # messages.warning(request, 'Este es un mensaje de advertencia.')
        # messages.info(request, 'Esto es solo información.')

        # Redirigir a otra vista
        if empleado_hospital:
            # Cambiar el estado a False

            ## VOY A MARCAR QUE EL USUARIO UYA SE REGISTRO Y VALIDO SU EMAIL 
            empleado_hospital.estado = True
            empleado_hospital.email_validado = True
            # Guardar los cambios

            empleado_hospital.save()
            ## VOY A VERIFICAR SI EXISTE EL USUARIO DE LO CONTRATRIO CREO EL USUARIO
            if User.objects.filter(email=PersonalHospital.email).exists():
                return JsonResponse({"error": "El usuario ya existe"}, status=400)


            # Generar contraseña aleatoria
            password = get_random_string(length=12)
            print(f'{empleado_hospital.email}')
            print(f'{password}')

            # Crear el usuario
            usuario = User.objects.create_user(
                username=empleado_hospital.email,
                email=empleado_hospital.email,
                password=password,
            )
            # Marcar como usuario activo y staff
            usuario.is_active = True
            usuario.is_staff = True  # Esto permitirá que acceda al panel de administración
            usuario.save()

            # Asignar el rol "usuario_institucional"
            try:
                grupo = Group.objects.get(name="usuario_institucional")
                usuario.groups.add(grupo)  # Asigna el grupo al usuario
            except:
                return JsonResponse({"error": "El grupo no existe no se puede agregar al grupo"}, status=400)  

            usuario.save()

            

            # (Opcional) Enviar la contraseña por correo
            send_mail(
                "Tu cuenta ha sido creada",
                f"Tu usuario: {empleado_hospital.email}\nTu contraseña: {password}",
                "noresponder@hospital.com",
                [empleado_hospital.email],
                fail_silently=False,
            )

            # return JsonResponse({"mensaje": "Usuario creado con éxito"}, status=201)
            messages.success(request, 'El registro se completo enviamos la clave de acceso a tu email !')
        else:
            messages.error(request, 'El registro a fallado, comunicarse con el administrador del sitio!')
        
    except:
        messages.error(request, 'Ocurrió un error. al intentar validar el usuario. comunicarse con el administrador del sitio')
    finally:
        return redirect('/')