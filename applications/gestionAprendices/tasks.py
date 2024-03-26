# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
# @shared_task

def send_welcome_email(email, nombres, numero_documento, default_password):
    # Construir el enlace de la página
    # Construir las URLs de la página
        frontend_url = 'http://tu_url_del_frontend.com'  # Reemplaza esto con la URL real de tu frontend
        welcome_page_url = f'{frontend_url}/welcome'  # URL para la página de bienvenida
        reset_password_url = f'{frontend_url}/reset_password'  # URL para restablecer la contraseña

        # Renderizar la plantilla HTML del correo electrónico
        html_message = render_to_string('email_template.html', {
            'nombres': nombres,
            'numero_documento': numero_documento,
            'default_password': default_password,
            'welcome_page_url': welcome_page_url,
            'reset_password_url': reset_password_url,
        })

        # Envío del correo electrónico al usuario aprendiz
        subject = '¡Bienvenido al Sistema SEEP!'
        from_email = 'seepsenacditi@gmail.com'
        to_email = [email]

        send_mail(subject, None, from_email, to_email, html_message=html_message)

