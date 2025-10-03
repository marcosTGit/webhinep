
from django.urls import path, include
from . import views

# SEGUNDO FACTOR DE AUTENTICACION DJANGO OTP
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views  #reset pass via mail 
import private_storage.urls



urlpatterns = [
    # path('login_institucional', views.login_institucional, name='login_institucional'),
    path('registrar_usuario_institucional', views.RegistrarUsuario, name='registrar_usuario_institucional'),
    path('validar-usuario-institucional/<str:token>', views.ValidarRegistro, name='ubicacion'), # GET
    path('private-media/', include(private_storage.urls)),
    path("private-media/<int:pk>", views.MyStorageView.as_view()),
]
