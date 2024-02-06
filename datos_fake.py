import random
from faker import Faker
from applications.gestionAprendices.models import Empresa, Ficha, Aprendiz, InstructorEncargado
from django.db.utils import IntegrityError

fake = Faker()

# Crear Empresas
empresas = []
for _ in range(8):
    empresa = Empresa(
        nit=fake.unique.random_int(min=1000000000, max=9999999999),
        razon_social=fake.company(),
        nombre_jefe_inmediato=fake.name(),
        correo=fake.company_email(),
        telefono=fake.phone_number(),
    )
    empresas.append(empresa)

Empresa.objects.bulk_create(empresas)

# Crear Fichas
fichas = []
for _ in range(5):
    ficha = Ficha(
        numero_ficha=fake.unique.random_int(min=10000, max=99999),
        nombre_programa=fake.job(),
        nivel_formacion=random.choice(['Técnico', 'Tecnólogo']),
        horario_formacion=random.choice(['Mixta', 'Diurna']),
        cantidad_aprendices=fake.random_int(min=10, max=30),
    )
    fichas.append(ficha)

Ficha.objects.bulk_create(fichas)

# Crear Aprendices
aprendices = []
for _ in range(30):
    try:
        aprendiz = Aprendiz(
            nombres=fake.first_name(),
            apellidos=fake.last_name(),
            tipo_documento=random.choice(['CC', 'TI']),
            numero_documento=fake.unique.random_int(min=10000000, max=99999999),
            fecha_expedicion=fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=40),
            lugar_expedicion=fake.city(),
            fecha_nacimiento=fake.date_of_birth(tzinfo=None, minimum_age=16, maximum_age=30),
            sexo=random.choice(['Masculino', 'Femenino']),
            direccion_domicilio=fake.address(),
            municipio=fake.city(),
            departamento=fake.state(),
            numero_celular1=fake.phone_number(),
            numero_celular2=fake.phone_number(),
            telefono_fijo=fake.phone_number(),
            correo_principal=fake.email(),
            correo_secundario=fake.email(),
            finalizacion_etapa_lectiva=fake.date_of_birth(tzinfo=None, minimum_age=16, maximum_age=25),
            estado_aprobacion=random.choice(['aprobado', 'no_aprobado', 'pendiente']),
            empresa=random.choice(empresas),
            ficha=random.choice(fichas),
        )
        aprendices.append(aprendiz)
    except IntegrityError:
        # Si se produce una excepción de integridad debido a valores duplicados, intentamos crear otro aprendiz.
        pass

Aprendiz.objects.bulk_create(aprendices)

# Crear Instructores
instructores = []
for _ in range(3):
    instructor = InstructorEncargado(
        nombres=fake.first_name(),
        apellidos=fake.last_name(),
        numero_documento=fake.unique.random_int(min=10000000, max=99999999),
        correo=fake.email(),
        telefono=fake.phone_number(),
        ficha=random.choice(fichas),
    )
    instructores.append(instructor)

InstructorEncargado.objects.bulk_create(instructores)

print("Datos falsos creados correctamente.")
