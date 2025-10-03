from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.
from .models import *
from institucional.models import *


# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

admin.site.site_header = "H.I.N.E.P - Panel de Administración Web"
admin.site.site_title = "HINEP WEB"
admin.site.index_title = "Bienvenido al Panel Admin"


# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
class NoticiaAdmin(admin.ModelAdmin):
    search_fields = ['titulo', 'fecha_publicacion']  # Campos a buscar (nombre y estado relacionado)
    list_display = ['fecha_publicacion', 'titulo']  # Campos que se muestran en el listado
    # list_editable = ['titulo', 'contenido']
    actions = ['previsualizar_noticia']
    # actions = ['exportar_xlsx']
    
    # 0000000000000000000000000000000000000000000000000000000000000000000000
    # 0000000000000000000000000000000000000000000000000000000000000000000000
    
    # class Media:
    #     js = ('gestionFlota/js/flota.js',)  # Ruta de tu script JavaScript

        
    # 0000000000000000000000000000000000000000000000000000000000000000000000
    # 0000000000000000000000000000000000000000000000000000000000000000000000
    def previsualizar_noticia(modeladmin, request, queryset):
        if queryset.count() == 1:  # Asegúrate de que solo se seleccione un registro
            noticia = queryset.first()
            url = reverse('mostrar_noticia', args=[noticia.token])  # Redirige a la vista de previsualización
            return HttpResponseRedirect(url)
        else:
            modeladmin.message_user(request, "Selecciona solo una noticia para previsualizar.", level="error")


    

    previsualizar_noticia.short_description = "Previsualizar Noticia"
    # PrevisualizarNoticia.short_description = "Previsualizar Noticia"
    # exportar_xlsx.short_description = "Exportar reporte en XLSX"
    
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
class ArchivoNoticiaInline(admin.TabularInline):  # También puedes usar StackedInline
    model = FileArticulo
    extra = 1  # Número de campos vacíos adicionales para cargar más archivos
    # fields = ("archivo")  # Solo mostrar el campo archivo


class ArticuloAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "registro_creado")
    search_fields = ["titulo", "autor__username"]
    inlines = [ArchivoNoticiaInline]  # Agrega la opción de subir archivos en la misma vista
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs  # Los administradores ven todo
    #     return qs.filter(autor=request.user)  # Los usuarios solo ven sus propias noticias

    list_filter = ['registro_creado', 'autor__username']
    # date_hierarchy = 'registro_creado'

    # 0000000000000000000000000000000000000000000000000000000000000000
    # 0000000000000000000000000000000000000000000000000000000000000000
    def has_delete_permission(self, request, obj=None):
        # Solo permite eliminar si el usuario es el autor
        if request.user.is_superuser:
            return super().has_delete_permission(request, obj)
        if obj and obj.autor != request.user:
            return False
        return super().has_delete_permission(request, obj)
    


    # def has_view_permission(self, request, obj=None):
    #     user = request.user
    #     # if private_file.owner == user:
    #     #     return True
            
    #     # 2. Los administradores pueden acceder (ya funciona)
    #     if user.is_staff:
    #         return True
    #     else:
    #         print("No es admin")                
    #     # 3. Agregar aquí otras condiciones según tu necesidad:
         
    #     # Ejemplo: Usuarios en mismo grupo/departamento
    #     if user.groups.filter(name='usuario_institucional').exists():
    #         return True
    #     else:
    #         print("no pretenece al grupo intitucionl")
         
    #     # Ejemplo: Usuarios con un permiso específico
    #     # if user.has_perm('mi_app.puede_ver_documentos'):
    #     #     return True
            
    #     # Ejemplo: Usuarios específicos por nombre
    #     if user.username in ['usuario1', 'prueba']:
    #         return True
    #     else:
    #         print("no esta enla lista permitica")
    #     return False

    # 0000000000000000000000000000000000000000000000000000000000000000
    # 0000000000000000000000000000000000000000000000000000000000000000
    def has_change_permission(self, request, obj=None):
        if obj and obj.autor != request.user:
            return False  # Solo el autor puede editar su noticia
        return True
    

    # 0000000000000000000000000000000000000000000000000000000000000000
    # 0000000000000000000000000000000000000000000000000000000000000000
    def save_model(self, request, obj, form, change):

        if not obj.autor:  # Solo asigna si no tiene un autor
            obj.autor = request.user
        obj.save()




# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
class PersonalHospitalAdmin(admin.ModelAdmin):
    list_display = ("numero_agente", "email", "estado")
    search_fields = ["numero_agente"]

# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
class SugerenciaAdmin(admin.ModelAdmin):
    search_fields = ['mensaje', 'usuario','sugerencia']  # Campos a buscar (nombre y estado relacionado)
    list_display = ['apellido_nombre', 'tipo_sugerencia', 'tipo_usuario']  # Campos que se muestran en el listado
    # list_editable = []
    readonly_fields = [f.name for f in Sugerencia._meta.fields]  # todos los campos en modo solo lectura
    
    def has_delete_permission(self, request, obj=None):
        # Solo permite eliminar si el usuario es el superusuario
        if request.user.is_superuser:
            return super().has_delete_permission(request, obj)
        return False
        



admin.site.register(Image)
admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(Slider)
admin.site.register(PersonalHospital, PersonalHospitalAdmin )
# admin.site.register(FileArticulo)
admin.site.register(Articulo, ArticuloAdmin)
admin.site.register(Sugerencia, SugerenciaAdmin)
