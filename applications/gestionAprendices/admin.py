from django.contrib import admin

from .models import InstructorEncargado , Ficha , Empresa, Aprendiz, DocumentacionAprendiz

class FichaAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero_ficha', 'nombre_programa', 'nivel_formacion', 'horario_formacion', 'cantidad_aprendices')

admin.site.register(Aprendiz)
admin.site.register(InstructorEncargado)
admin.site.register(Ficha, FichaAdmin)
admin.site.register(Empresa)
admin.site.register(DocumentacionAprendiz)

