from django.core.mail import send_mail
from django.http import HttpResponse

def enviar_correo(request):
    send_mail(
        'Prueba',
        'Hola mundo.',
        'seepsenacditi@gmail.com',
        ['nyamoli213@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse('Correo enviado exitosamente.')

# from django.shortcuts import render
# from django.http import HttpResponse
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# def enviar_correo_personalizado(request):
#     # Definir los detalles del correo electrónico
#     remitente = 'seepsenacditi@gmail.com'
#     destinatario = 'nyamoli213@gmail.com'
#     asunto = 'Asunto del correo'
#     mensaje = 'Este es el mensaje por defecto.'

#     # Crear el objeto MIMEMultipart para el correo electrónico
#     msg = MIMEMultipart()
#     msg['From'] = remitente
#     msg['To'] = destinatario
#     msg['Subject'] = asunto

#     # Agregar el mensaje al cuerpo del correo electrónico
#     msg.attach(MIMEText(mensaje, 'plain'))

#     # Configurar la conexión SMTP
#     servidor_smtp = 'smtp.email.com'
#     puerto_smtp = 587
#     usuario_smtp = 'seepsenacditi@gmail.com'
#     contrasena_smtp = 'ajmwhungdpbswfmp'

#     try:
#         # Iniciar la conexión SMTP
#         servidor = smtplib.SMTP(host=servidor_smtp, port=puerto_smtp)
#         servidor.starttls()
#         servidor.login(usuario_smtp, contrasena_smtp)

#         # Enviar el correo electrónico
#         servidor.sendmail(remitente, destinatario, msg.as_string())

#         # Cerrar la conexión SMTP
#         servidor.quit()

#         return HttpResponse('Correo enviado exitosamente.')
#     except Exception as e:
#         return HttpResponse('Error al enviar el correo: {}'.format(str(e)))
