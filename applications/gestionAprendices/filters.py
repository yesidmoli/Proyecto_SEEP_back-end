import django_filters
from .models import Aprendiz

class AprendizFilter(django_filters.FilterSet):
    numero_ficha = django_filters.CharFilter(field_name='ficha__numero_ficha')
    estado_aprobacion = django_filters.ChoiceFilter(
        field_name='estado_aprobacion',
        choices=(('aprobado', 'Aprobado'), ('no_aprobado', 'No Aprobado'), ('pendiente', 'Pendiente'))
    )

    class Meta:
        model = Aprendiz
        fields = ['numero_ficha', 'estado_aprobacion']