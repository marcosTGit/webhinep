import json
from django.contrib import messages  # importamos lo smensajes flash
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re
import uuid
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from .api_get import getMenuPortalAPi, getContenidoURL, leerJsonConvertirtojson
from .forms import * # ContactoForm, ImageForm  # importamos lo sformularios
from .models import * # Image, Suscriptos, Noticia # imprtamos los modelos
from .helpers import * # 

# from django_otp.decorators import otp_required
# @otp_required


# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000


def procesar_contenido(contenido):
    # Reemplazar saltos de línea \n con <br>
    # contenido = contenido.replace("\\n", "<br>")

    # Reemplazar texto entre * * por <strong>
    contenido = re.sub(r'\*(.*?)\*', r'<strong>\1</strong>', contenido)

    # Convertir #http://www.url@texto# a un enlace HTML
    contenido = re.sub(
        r'#(http[s]?://[^\s]+)@([^#]+)#',
        r'<a href="\1" target="_blank">\2</a>',
        contenido
    )

    # Devolver como HTML seguro
    return mark_safe(contenido)



# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

menu = getMenuPortalAPi
cantidad_noticias=6
mas_noticias = getContenidoURL("https://api-portal.catamarca.gob.ar/api/v1/noticia/?include=categoria,organismo&contenido_titulo=salud&organismo_id=&categoria_id=&tags=&page[number]=1&page_size=6&ordering=-fecha_creado")
data ={
    'form_contacto' : ContactoForm(),
    'form_sugerencia' : SugerenciaForm(),
    'menu' : menu,
    'autoridades':{
        "direccion_general":"Dra. Graciela Romero",
        "direccion_administrativa":"CPN. Lorena Ponce",
        "direccion_asistencial":"Dra. Patricia Rojas",
        "direccion_mantenimiento":"MMO. Martin Quevedo",
        },
    'mas_noticias' : mas_noticias,
}
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

def CargarValores(template=False, noticia=False):


    data["template"]=template
    data['imagenes'] = Image.objects.all()
    # data['sliders'] = Slider.objects.all()
    data['sliders'] = Slider.objects.filter(
        publicacion_activa=True,
        fecha_publicacion__lte= now()).filter(
        Q(fin_publicacion__gte=now()) | Q(fin_publicacion__isnull=True)
    )
    # data['noticias'] = Noticia.objects.filter(publicacion_activa=True)
    data['noticias'] = Noticia.objects.filter(
        publicacion_activa=True,
        fecha_publicacion__lte= now()).filter(
        Q(fin_publicacion__gte=now()) | Q(fin_publicacion__isnull=True)
    )
    data['noticia'] = noticia

# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
def Index(request):
    CargarValores()
    return render(request, 'web/index.html', data)


# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
def Request_Controller(request):
    CargarValores(f"web/{request.resolver_match.url_name}.html")
    return render(request, 'web/index.html', data)


# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# @csrf_exempt  # Usar solo si estás haciendo pruebas. Mejor usar csrf_token en el template.
def Contacto(request):
    try:
        if request.method == 'POST' and request.POST.get('name') and request.POST.get('email') and request.POST.get('mensaje') and request.POST.get('csrfmiddlewaretoken'):
            return JsonResponse({'message': 'Datos recibidos correctamente'})
        else:
            return JsonResponse({'message': 'me esta falatndo algo'})
    except:
        return JsonResponse({'error': 'Metodo no permitido'}, status=405)
    
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# @csrf_exempt  # Usar solo si estás haciendo pruebas. Mejor usar csrf_token en el template.
def RegistrarSugerencia(request):
    try:
        datos=json.loads(request.body)
        if request.method == 'POST' and datos['csrfmiddlewaretoken']: # los datos estan
            # ahora intentamos almancendar en la base de datos con validacion incluida
            try:
                validate_email(datos['email'])
                email = datos['email']
            except ValidationError:
                email = "sin@mail.com"
            
            sugerencia = Sugerencia.objects.create(
                apellido_nombre =datos['apellido_nombre'],
                telefono = str(datos['telefono']),
                email = email,
                tipo_usuario =datos['tipo_usuario'],
                tipo_sugerencia =datos['tipo_sugerencia'],
                mensaje =datos['mensaje'],
                )
            
            if not sugerencia:  # SI NO SE CREO EL REGISTRO DEVUELVE ERROR
                return JsonResponse({"error": "Datos incorrectos."}, status=400)
            # a estas instancias ya esta creado el registro
            return JsonResponse({"mensaje": "Sugerencia registrada!"}, status=201)
        else:
            # faltan parametros
            return JsonResponse({"error": "datos incorrectos"}, status=400)
            # return JsonResponse({'message': 'me esta falatndo algo'})
    except:
        return JsonResponse({'error': 'Metodo no permitido'}, status=405)



# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# @csrf_exempt  # Usar solo si estás haciendo pruebas. Mejor usar csrf_token en el template.
def Suscribir(request):
    try:
        datos=json.loads(request.body)
        # print(datos)
        if request.method == 'POST' and datos['email'] and datos['token']: # los datos estan
            # ahora intentamos almancendar en la base de datos con validacion incluida
            try:
                validate_email(datos['email'])
            except ValidationError:
                return JsonResponse({"error": "El formato del email no es válido."}, status=400)
            # print("intentantdo crear ")
            suscripto, creado = Suscriptos.objects.get_or_create(email=datos['email'])
            # print("registro creado  ")
            # return JsonResponse({'message': 'Datos recibidos correctamente'})
            if not creado:  # SI NO SE CREO EL REGISTRO DEVUELVE ERROR
                return JsonResponse({"error": "El email ya está registrado."}, status=400)
            # a estas instancias ya esta creado el registro
            return JsonResponse({"mensaje": "Suscripción exitosa."}, status=201)
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
def MostrarNoticia(request, token_noticia=False):
    try:
        uuid.UUID(token_noticia) # intenta validar el valor uuid

        data['noticia_portal'] = False
        if not str(request.user) == "AnonymousUser" and token_noticia:
            try:
                noticia_requerida = Noticia.objects.get(token=token_noticia)
                noticia_requerida.contenido = procesar_contenido(noticia_requerida.contenido)
                noticia_requerida.contenido_destacado = procesar_contenido(noticia_requerida.contenido_destacado)
                CargarValores(False, noticia_requerida)
                return render(request, "web/noticia.html", data)
            except:
                CargarValores()
                messages.warning(request, "Contenido no disponible")
                return render(request, "web/noticia.html", data)

        else:
            if token_noticia:
                try:
                    noticia_requerida = Noticia.objects.get(token=token_noticia, publicacion_activa=True)
                    CargarValores(noticia=noticia_requerida)
                except:
                    return redirect('/')
    except:
        if token_noticia:
            # messages.warning(request, f"{token_noticia} no es un id valido ")
            try:
                noticia_portal = getContenidoURL(f"https://api-portal.catamarca.gob.ar/api/v1/noticia/{token_noticia}")
                data['noticia_portal'] = noticia_portal['data']['attributes']
                return render(request, "web/noticia.html", data)
            except:
                messages.warning(request, f"Contenido no disponible")
                return redirect('/')
        else:
            CargarValores()
            return render(request, "web/noticia.html", data)



# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# @csrf_exempt  # Usar solo si estás haciendo pruebas. Mejor usar csrf_token en el template.
def ValidarSuscripcion(request, validar_token):

    # Obtener el registro específico
    try:
        suscripto = Suscriptos.objects.get(token=validar_token)
        # messages.warning(request, 'Este es un mensaje de advertencia.')
        # messages.info(request, 'Esto es solo información.')

        # Redirigir a otra vista
        if suscripto:
            # Cambiar el estado a False
            suscripto.estado = True
            # Guardar los cambios
            suscripto.save()
            messages.success(request, 'La Suscripcion se realizó con éxito. puedes desvincularte cuando quieras!')

    except:
        messages.error(request, 'Ocurrió un error. La devinculacion falló.')
    finally:
        return redirect('/')


# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# @csrf_exempt  # Usar solo si estás haciendo pruebas. Mejor usar csrf_token en el template.
def DesvincularBoletin(request, desvincular_token):

    try:
        suscripto = Suscriptos.objects.get(token=desvincular_token)
        # messages.warning(request, 'Este es un mensaje de advertencia.')
        # messages.info(request, 'Esto es solo información.')

        # Redirigir a otra vista
        if suscripto:
            # Cambiar el estado a False
            suscripto.estado = False
            # Guardar los cambios
            suscripto.save()
            messages.success(request, 'La devinculacion se realizó con éxito.')

    except:
        messages.error(request, 'Ocurrió un error. La devinculacion falló.')
    finally:
        return redirect('/')






# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
def ContenidoApiPortal(request, recurso, seccion=None, subseccion=None,id=False):
    # url="https://api-portal.catamarca.gob.ar/api/v1/noticia/?include=categoria,organismo&contenido_titulo=salud&organismo_id=&categoria_id=&tags=&page[number]=1&page_size=16&ordering=-fecha_creado"
    url=f"https://api-portal.catamarca.gob.ar/api/v1/cms/seccion/?pagina_id={id}&include=contenidos"
    data["contenido"]=getContenidoURL(url)
    CargarValores()
    return render(request, 'web/contenido_portal.html', data)


# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

# def getGaleria(request):
#     data["images"] = Image.objects.all()
#     return render(request, 'web/galeria.html', {'images': data})


# # 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# # 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

# def upload_image(request):
#     data["form_imgupload"]=ImageForm()

#     # if request.method == 'POST':
#     #     form = ImageForm(request.POST, request.FILES)
#     #     if form.is_valid():
#     #         form.save()
#     #         return redirect('galeria')
#     # else:
#     #     form = ImageForm()
#     return render(request, 'web/img_upload.html', data)


# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
def custom_403_view(request, exception):
    return render(request, 'web/error_403.html', status=403)

def custom_404_view(request, exception):
    return render(request, 'web/error_404.html', status=404)

def custom_500_view(request):
    return render(request, 'web/error_500.html', status=500)

from django.contrib.auth.views import PasswordResetView
from django.urls import path
class CustomPasswordResetView(PasswordResetView):
    email_template_name = "registration/password_reset_email.txt"
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    # template_name = "registration/password_reset_form.html"


# class CustomPasswordResetView(PasswordResetView):
#     email_template_name = 'web/registration/password_reset_email.html'
#     subject_template_name = 'web/registration/password_reset_subject.txt'


# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
def Test(request, id=1288):

    # send_notification_email('marcossebastiant@gmail.com','mtoledo', {
    #     'title': 'tiutlo de prueba',
    #     'message': 'message de prueba',
    #     'date': '2025-09-08'
    # })

    # send_vinculation_email("marcossebastiant@gmail.com", "mtoledo",{
    #     'platform_name': 'HINEP.WEB',
    #     'role': 'mtoledo',
    #     'expiration_date': '24ha',
    #     'vinculation_url': 'HINEP.WEB'
    # })


    # return JsonResponse({'menu': getMenuPortalAPi()})
    url=f"https://api-portal.catamarca.gob.ar/api/v1/cms/seccion/?pagina_id={id}&include=contenidos"
    data['contenido']=getContenidoURL(url)
    return render(request, 'web/test.html', data)


def Testjson(request, id):
# def Testjson(request):
    # id=1288
    url=f"https://api-portal.catamarca.gob.ar/api/v1/cms/seccion/?pagina_id={id}&include=contenidos"
    data=getContenidoURL(url)
    return JsonResponse(data)
    # 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    # 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    # 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    # return render(request, 'web/test.html', data)
    # 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    # 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
    data = getMenuPortalAPi()
    return JsonResponse({"data": data})
