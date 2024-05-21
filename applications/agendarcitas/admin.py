from django.contrib import admin

from applications.agendarcitas.models.visita import Visita


class VisitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_visita', 'tipo_visita', 'numero_visita', 'aprendiz', 'lugar', 'estado')
    search_fields = ('tipo_visita', 'lugar', 'numero_visita')
    list_display_links = ('id', 'tipo_visita')
    list_filter = ('fecha_visita', 'estado', 'numero_visita')
    
admin.site.register(Visita, VisitaAdmin)
