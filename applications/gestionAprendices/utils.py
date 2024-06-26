from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from applications.gestionAprendices.models.models import Aprendiz, Documentos

def enviar_alertas_documentos_faltantes(id_ficha):
    try:
        aprendices = Aprendiz.objects.filter(ficha__id=id_ficha)

        for aprendiz in aprendices:
            documentos_faltantes = obtener_documentos_faltantes(aprendiz)
            if documentos_faltantes:
                mensaje_html = construir_mensaje_html(documentos_faltantes, aprendiz)
                enviar_correo(aprendiz.correo_principal, 'Alerta: Documentos Faltantes', mensaje_html)

        return True
    except Exception as e:
        print(f'Error al enviar alertas: {e}')
        return False

def obtener_documentos_faltantes(aprendiz):
    documentos_obligatorios = ['Documento de identidad', 'Carta Laboral', 'Certificado Agencia Publica', 'Carnet Destruido', 'Pruebas TyT']
    documentos_tecnologo = ['Pruebas TyT']
    documentos_faltantes = []

    for documento in documentos_obligatorios:
        if not Documentos.objects.filter(aprendiz=aprendiz, tipo_documento=documento).exists():
            documentos_faltantes.append(documento)

    if aprendiz.ficha.nivel_formacion == 'Tecnólogo':
        for documento in documentos_tecnologo:
            if not Documentos.objects.filter(aprendiz=aprendiz, tipo_documento=documento).exists():
                documentos_faltantes.append(documento)

    return documentos_faltantes

def construir_mensaje_html(documentos_faltantes, aprendiz):
    context = {
        'aprendiz_nombre': aprendiz.nombres,
        'aprendiz_apellidos': aprendiz.apellidos,
        'documentos_faltantes': documentos_faltantes
    }
    return render_to_string('emails/documentos_faltantes.html', context)

def enviar_correo(destinatario, asunto, mensaje_html):
    try:
        # Renderizar plantilla HTML
        plain_message = strip_tags(mensaje_html)  # Mensaje en texto plano para clientes de correo que no soportan HTML
        send_mail(asunto, plain_message, 'seepsenacditi@gmail.com', [destinatario], html_message=mensaje_html)
        return True
    except Exception as e:
        print(f'Error al enviar correo a {destinatario}: {e}')
        return False
