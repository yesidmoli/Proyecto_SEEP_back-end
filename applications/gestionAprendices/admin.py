from django.contrib import admin

from .models.models import InstructorEncargado , Ficha , Empresa, Aprendiz, DocumentacionAprendiz, Documentos

class FichaAdmin(admin.ModelAdmin):
    list_display = ( 'numero_ficha', 'nombre_programa', 'nivel_formacion', 'horario_formacion')

admin.site.register(Aprendiz)
admin.site.register(InstructorEncargado)
admin.site.register(Ficha, FichaAdmin)
admin.site.register(Empresa)
# admin.site.register(DocumentacionAprendiz)
admin.site.register(Documentos)






