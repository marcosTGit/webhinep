"""
URL configuration for hinep project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf.urls import handler404, handler403, handler500
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from django.urls import path, include
from django.contrib import admin
# from web import views
from django.contrib.auth import views as auth_views  #reset pass via mail

# 000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000
from two_factor.urls import urlpatterns as tf_urls


# 000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000
# 000000000000000000000000000000000000000000000000000

from web.views import CustomPasswordResetView


urlpatterns = [
    path('accounts/profile/', admin.site.urls, name='paneladmin'),
    # path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('', include(tf_urls)),  # Incluye las vistas de Two-Factor Auth
    path('', include('web.urls')),  # Incluye las URLs de la app `pagina`
    path('', include('institucional.urls')),  # Incluye las URLs de la app `pagina`
    path("private-media/", include("private_storage.urls")),  # 👈 IMPORTANTE


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "web.views.custom_404_view"
handler403 = 'web.views.custom_403_view'
handler500 = 'web.views.custom_500_view'
