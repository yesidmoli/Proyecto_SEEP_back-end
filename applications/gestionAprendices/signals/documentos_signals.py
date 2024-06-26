from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from applications.gestionAprendices.models.models import Documentos
import mimetypes
from django.template.loader import render_to_string

@receiver(post_save, sender=Documentos)
def enviar_correo_instructor(sender, instance, created, **kwargs):
    aprendiz = instance.aprendiz
    ficha = aprendiz.ficha
    instructor_encargado = ficha.instructores.first()
    
    if instructor_encargado:
        email_instructor = instructor_encargado.correo
        nombre_aprendiz = f"{aprendiz.nombres} {aprendiz.apellidos}"

        if created:
            asunto = 'Nuevo Documento Cargado'
            template = 'emails/nuevo_documento.html'
        else:
            asunto = 'Documento Actualizado'
            template = 'emails/documento_actualizado.html'
        
        contexto = {
            'nombre_aprendiz': nombre_aprendiz,
            'tipo_documento': instance.tipo_documento,
            'observaciones': instance.observaciones,
        }

        mensaje_html = render_to_string(template, contexto)
        destinatario = [email_instructor]

        email = EmailMessage(
            asunto,
            mensaje_html,
            'seepsenacditi@gmail.com',
            destinatario
        )
        email.content_subtype = 'html'  # Para que el correo se envíe en formato HTML

        if instance.archivo:
            mime_type, _ = mimetypes.guess_type(instance.archivo.path)
            email.attach(instance.archivo.name, instance.archivo.read(), mime_type)

        email.send()
