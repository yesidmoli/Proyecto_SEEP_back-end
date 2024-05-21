from django.contrib import admin

from .models.models import InstructorEncargado , Ficha , Empresa, Aprendiz, DocumentacionAprendiz, Documentos

class FichaAdmin(admin.ModelAdmin):
    list_display = ( 'numero_ficha', 'nombre_programa', 'nivel_formacion', 'horario_formacion')



class AprendizAdmin(admin.ModelAdmin):
    list_display = ('id','numero_documento', 'nombres', 'apellidos', 'correo_principal', 'ficha', 'empresa', 'estado_aprobacion')
    search_fields = ('numero_documento', 'nombres', 'apellidos', 'correo_principal')
    list_display_links= ('id', 'numero_documento','nombres')
    list_filter = ('estado_aprobacion', 'ficha', 'empresa')
   
class InstructorEncargadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombres', 'apellidos', 'correo', 'telefono')
    search_fields = ('nombres', 'apellidos', 'correo')
    list_display_links = ('id', 'nombres')
     
class FichaAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero_ficha', 'nombre_programa', 'nivel_formacion', 'horario_formacion')
    search_fields = ('numero_ficha', 'nombre_programa')
    list_display_links = ('id', 'numero_ficha')
    list_filter = ('numero_ficha',)
    
    
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id', 'razon_social', 'nit', 'direccion', 'telefono', 'correo')
    search_fields = ('razon_social', 'nit')
    list_display_links = ('id', 'razon_social')
    list_filter = ('razon_social',)
    
class DocumentacionAprendizAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo_documento', 'aprendiz','is_bitacora')
    search_fields = ('tipo_documento', 'aprendiz')
    list_display_links = ('id', 'tipo_documento')
    list_filter = ('aprendiz', 'tipo_documento')
    
admin.site.register(Aprendiz, AprendizAdmin)
admin.site.register(InstructorEncargado, InstructorEncargadoAdmin)
admin.site.register(Ficha, FichaAdmin)
admin.site.register(Empresa, EmpresaAdmin)

# admin.site.register(DocumentacionAprendiz)
admin.site.register(Documentos, DocumentacionAprendizAdmin)






