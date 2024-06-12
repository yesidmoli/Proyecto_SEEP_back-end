# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models.visita import Visita

@receiver(post_save, sender=Visita)
def enviar_notificacion_visita(sender, instance, created, **kwargs):
    if created:
        asunto = 'Nueva visita programada'
        mensaje_texto = f'Se ha programado una nueva visita para el aprendiz {instance.aprendiz.nombres}. Fecha: {instance.fecha_visita}, Hora: {instance.hora_visita}, Lugar: {instance.lugar}, Estado: {instance.estado}, Tipo: {instance.tipo_visita}.'
        mensaje_html = render_to_string('emails/nueva_visita.html', {'aprendiz': instance.aprendiz, 'fecha_visita': instance.fecha_visita, 'hora_visita': instance.hora_visita, 'lugar': instance.lugar, 'estado': instance.estado, 'tipo_visita': instance.tipo_visita})
    else:
        asunto = 'Visita actualizada'
        mensaje_texto = f'Se ha actualizado la visita del aprendiz {instance.aprendiz.nombres}. Nueva Fecha: {instance.fecha_visita}, Nueva Hora: {instance.hora_visita}, Lugar: {instance.lugar}, Estado: {instance.estado}, Tipo: {instance.tipo_visita}.'
        mensaje_html = render_to_string('emails/visita_actualizada.html', {'aprendiz': instance.aprendiz, 'fecha_visita': instance.fecha_visita, 'hora_visita': instance.hora_visita, 'lugar': instance.lugar, 'estado': instance.estado, 'tipo_visita': instance.tipo_visita})
    
    send_mail(
        asunto,
        mensaje_texto,
        'seepsenacditi@gmail.com',  # El remitente
        [instance.aprendiz.correo_principal],  # El destinatario
        fail_silently=False,
        html_message=mensaje_html,  # Mensaje HTML
    )