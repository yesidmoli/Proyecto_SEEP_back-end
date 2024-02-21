import json
from datetime import datetime
from applications.gestionAprendices.models.models import Empresa, Ficha, Aprendiz, InstructorEncargado

# Cargar datos desde el archivo JSON
with open('datos_falsos.json', 'r') as file:
    data = json.load(file)

# Crear empresas
empresas = {}
for empresa_data in data['empresas']:
    empresa, created = Empresa.objects.get_or_create(nit=empresa_data['nit'], defaults=empresa_data)
    empresas[empresa_data['nit']] = empresa

# Crear fichas
for ficha_data in data['fichas']:
    empresa = empresas[ficha_data['empresa']['nit']]
    ficha_data['empresa'] = empresa
    ficha, created = Ficha.objects.get_or_create(numero_ficha=ficha_data['numero_ficha'], defaults=ficha_data)


# Crear aprendices
for aprendiz_data in data['aprendices']:
    aprendiz_data['empresa'] = empresas[aprendiz_data['empresa']['nit']]
    aprendiz, created = Aprendiz.objects.get_or_create(numero_documento=aprendiz_data['numero_documento'], defaults=aprendiz_data)

# Crear instructores encargados
for instructor_data in data['instructores']:
    instructor_data['ficha'] = Ficha.objects.get(numero_ficha=instructor_data['ficha']['numero_ficha'])
    instructor, created = InstructorEncargado.objects.get_or_create(numero_documento=instructor_data['numero_documento'], defaults=instructor_data)

