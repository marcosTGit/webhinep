
from django.urls import path
from . import views

# SEGUNDO FACTOR DE AUTENTICACION DJANGO OTP
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views  #reset pass via mail 


urlpatterns = [
    path('', views.Index, name='index'),


    path('contacto', views.Contacto, name='contacto'), # POST
    path('historia', views.Request_Controller, name='historia'), # GET
    path('nuestra_funcion', views.Request_Controller, name='nuestra_funcion'), #  GET
    path('autoridades', views.Request_Controller, name='autoridades'), # GET
    path('ubicacion', views.Request_Controller, name='ubicacion'), # GET
    path('<str:recurso>/<str:seccion>/<int:id>', views.ContenidoApiPortal, name='contenido_portal'), # GET 
    path('<str:recurso>/<str:seccion>/<int:id>', views.ContenidoApiPortal, name='contenido_portal'), # GET 
    path('<str:recurso>/<str:seccion>/<str:subseccion>/<int:id>', views.ContenidoApiPortal, name='contenido_portal'), # GET 
    path('noticia/<str:token_noticia>', views.MostrarNoticia, name='mostrar_noticia'),
    path('noticias/', views.MostrarNoticia, name='noticias'),
    path('portal_noticia/<str:id_noticia>', views.MostrarNoticia, name='contacto'),
     # 0000000000000000000000000000000000000000000000000000000000000
    path('suscribir', views.Suscribir, name='suscribir'),
    path('sugerencia', views.RegistrarSugerencia, name='suscribir'),
    path('validar-suscripcion/<str:validar_token>', views.ValidarSuscripcion, name='ubicacion'), # GET
    path('desvincular-boletin/<str:desvincular_token>', views.DesvincularBoletin, name='ubicacion'), # GET
     # 0000000000000000000000000000000000000000000000000000000000000
    path('test', views.Test, name='test'), # GET
    path('test/<int:id>', views.Test, name='test'), # GET
    path('testjson/<int:id>', views.Testjson, name='test'), # GET
    path('testjson', views.Testjson, name='test'), # GET

    # SEGUNDO FACTOR DE AUTENTICACION 
    # path('', include('django.contrib.auth.urls')),  # Autenticación estándar de Django
        # Restablecimiento de contraseña
    # path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        html_email_template_name="registration/password_reset_email.html",
        template_name = "registration/password_reset_form.html"
        ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name = "registration/password_reset_done.html"
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name = "registration/password_reset_confirm.html"
    ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name = "registration/password_reset_complete.html"
    ), name='password_reset_complete'),

    path('accounts/profile/logout/', auth_views.LogoutView.as_view(
        template_name = "registration/logged_out.html"
    ), name='logged_out'),

    
    
    
    
]
