from rest_framework import serializers

from ..models.formatoModels import *
from applications.gestionAprendices.serializers.serializers import AprendizSerializer, FichaSerializer, EmpresaSerializer
from applications.gestionAprendices.models.models import Aprendiz, Ficha, Empresa

class EvaluacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluacion
        fields = '__all__'


class ActividadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividades
        fields = '__all__'


class PlaneacionSerializer(serializers.ModelSerializer):
    actividades = ActividadesSerializer(many=True)

    class Meta:
        model = Planeacion
        fields = '__all__'

    def create(self, validated_data):
        actividades_data = validated_data.pop('actividades', [])
        planeacion = Planeacion.objects.create(**validated_data)

        for actividad_data in actividades_data:
            # Crear la actividad asociada a la planeación
            actividad_instance = Actividades.objects.create(**actividad_data)
            # Agregar la actividad creada a la relación ManyToMany de la planeación
            planeacion.actividades.add(actividad_instance)

        return planeacion

    def update(self, instance, validated_data):
        actividades_data = validated_data.pop('actividades', None)

        # Actualizar otros campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Actualizar las actividades solo si se proporcionaron nuevos datos de actividades
        if actividades_data is not None:
            # Limpiar las actividades actuales y agregar las nuevas
            instance.actividades.clear()
            for actividad_data in actividades_data:
                actividad_instance = Actividades.objects.create(**actividad_data)
                instance.actividades.add(actividad_instance)

        return instance



class FactoresActiCompSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorActitudinal
        fields = '__all__'


class FactoresTecnicosSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorTecnico
        fields = '__all__'


class SeguimientoSerializer(serializers.ModelSerializer):
    factores_actitudinales = FactoresActiCompSerializer(many=True)
    factores_tecnicos = FactoresTecnicosSerializer(many=True)

    class Meta:
        model = Seguimiento
        fields = '__all__'
        
    def create(self, validated_data):
        factores_actitudinales_data = validated_data.pop('factores_actitudinales', [])
        factores_tecnicos_data = validated_data.pop('factores_tecnicos', [])
        seguimiento = Seguimiento.objects.create(**validated_data)

        for factor_actitudinal_data in factores_actitudinales_data:
            factor_actitudinal_instance = FactorActitudinal.objects.create(**factor_actitudinal_data)
            seguimiento.factores_actitudinales.add(factor_actitudinal_instance)

        for factor_tecnico_data in factores_tecnicos_data:
            factor_tecnico_instance = FactorTecnico.objects.create(**factor_tecnico_data)
            seguimiento.factores_tecnicos.add(factor_tecnico_instance)

        return seguimiento

    def update(self, instance, validated_data):
        factores_actitudinales_data = validated_data.pop('factores_actitudinales', None)
        factores_tecnicos_data = validated_data.pop('factores_tecnicos', None)

        # Actualizar otros campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Actualizar los factores actitudinales solo si se proporcionaron nuevos datos de factores actitudinales
        if factores_actitudinales_data is not None:
            # Limpiar los factores actitudinales actuales y agregar los nuevos
            instance.factores_actitudinales.clear()
            for factor_actitudinal_data in factores_actitudinales_data:
                factor_actitudinal_instance = FactorActitudinal.objects.create(**factor_actitudinal_data)
                instance.factores_actitudinales.add(factor_actitudinal_instance)

        # Actualizar los factores técnicos solo si se proporcionaron nuevos datos de factores técnicos
        if factores_tecnicos_data is not None:
            # Limpiar los factores técnicos actuales y agregar los nuevos
            instance.factores_tecnicos.clear()
            for factor_tecnico_data in factores_tecnicos_data:
                factor_tecnico_instance = FactorTecnico.objects.create(**factor_tecnico_data)
                instance.factores_tecnicos.add(factor_tecnico_instance)

        return instance

class FormatoSerializer(serializers.ModelSerializer):
    planeacion = PlaneacionSerializer()
    seguimiento = SeguimientoSerializer()
    evaluacion = EvaluacionSerializer()
    aprendiz_data = AprendizSerializer(source='aprendiz', read_only=True)
    # aprendiz = AprendizSerializer(read_only=True)
    # aprendiz_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Aprendiz.objects.all(),
    #     source='aprendiz',
    #     write_only=True
    # )

    class Meta:
        model = FormatoPlaneacion
        fields = '__all__'


    def create(self, validated_data):

        """Obtenemos los datos que se envian en el json de cada modelo relacionado """
        planeacion_data = validated_data.pop('planeacion')
        seguimiento_data = validated_data.pop('seguimiento')
        evaluacion_data = validated_data.pop('evaluacion')
        

        #obtenemos las actividades que llegan desde el json y asi mismo los factores actitudinales y tecnicos
        actividades_data = planeacion_data.pop('actividades', [])
        factores_actitudinales_data = seguimiento_data.pop('factores_actitudinales', [])
        factores_tecnicos_data = seguimiento_data.pop('factores_tecnicos', [])


        #creamos las instancias segun con los datos obtenidos
        planeacion_instance = Planeacion.objects.create(**planeacion_data)
        seguimiento_instance = Seguimiento.objects.create(**seguimiento_data)
        evaluacion_instance = Evaluacion.objects.create(**evaluacion_data)

        # Asociar actividades con la instancia de Planeacion
        for actividad_data in actividades_data:

            #creamos la instancia de actividades
            actividad_instance = Actividades.objects.create(**actividad_data)

            #la asignamos a la instancia de planeacion
            planeacion_instance.actividades.add(actividad_instance)

        # Asociar factores actitudinales con la instancia de Seguimiento
        for factor_actitudinal_data in factores_actitudinales_data:
            factor_actitudinal_instance = FactorActitudinal.objects.create(**factor_actitudinal_data)
            seguimiento_instance.factores_actitudinales.add(factor_actitudinal_instance)

        # Asociar factores técnicos con la instancia de Seguimiento
        for factor_tecnico_data in factores_tecnicos_data:
            factor_tecnico_instance = FactorTecnico.objects.create(**factor_tecnico_data)
            seguimiento_instance.factores_tecnicos.add(factor_tecnico_instance)

        #devolvemos  la creacion del las instancias del serializador y el resto de los datos.
        return FormatoPlaneacion.objects.create(
            planeacion=planeacion_instance,
            seguimiento=seguimiento_instance,
            evaluacion=evaluacion_instance,
            **validated_data
        )
    
    def update(self, instance, validated_data):
        planeacion_data = validated_data.pop('planeacion', {})
        seguimiento_data = validated_data.pop('seguimiento', {})
        evaluacion_data = validated_data.pop('evaluacion', {})

        planeacion_instance = instance.planeacion
        seguimiento_instance = instance.seguimiento
        evaluacion_instance = instance.evaluacion

        # Actualizar la instancia de Planeacion

        """attr = clave value = valor"""
        for attr, value in planeacion_data.items():
            # Verificar si el atributo es 'actividades'
            if attr == 'actividades':
                # Limpiar las actividades actuales y agregar las nuevas
                planeacion_instance.actividades.clear()
                for actividad_data in value:
                    actividad_instance = Actividades.objects.create(**actividad_data)
                    planeacion_instance.actividades.add(actividad_instance)
            else:
                """objeto, clave (atributo) y el valor """
                setattr(planeacion_instance, attr, value)
        planeacion_instance.save()

        # Actualizar la instancia de Seguimiento
        for attr, value in seguimiento_data.items():

            if attr == "factores_actitudinales":
                seguimiento_instance.factores_actitudinales.clear()
                for factor_actitudinal_data in value:
                    factor_actitudinal_instance = FactorActitudinal.objects.create(**factor_actitudinal_data)
             
                    seguimiento_instance.factores_actitudinales.add(factor_actitudinal_instance)

            elif attr == "factores_tecnicos":
                seguimiento_instance.factores_tecnicos.clear()

                for factor_tecnico_data in value:
                    factor_tecnico_instance = FactorTecnico.objects.create(**factor_tecnico_data)
                    seguimiento_instance.factores_tecnicos.add(factor_tecnico_instance)
            else:
                setattr(seguimiento_instance, attr, value)
        seguimiento_instance.save()

        # Actualizar la instancia de Evaluacion
        for attr, value in evaluacion_data.items():
            setattr(evaluacion_instance, attr, value)
        evaluacion_instance.save()

        # Actualizar el resto de los datos de FormatoPlaneacion
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
    


# class FormatoPlaneacionSerializer(serializers.ModelSerializer):
#     seguimientos = SeguimientoSerializer(many=True, read_only=True)
#     evaluaciones = EvaluacionSerializer(many=True, read_only=True)
#     planeaciones = PlaneacionSerializer(many=True, read_only=True)

#     class Meta:
#         model = FormatoPlaneacion
#         fields = '__all__'


class AprendizCompletoSerializer(serializers.ModelSerializer):
    planeacion = serializers.SerializerMethodField()
    seguimiento = serializers.SerializerMethodField()
    evaluacion = serializers.SerializerMethodField()
    ficha = serializers.SerializerMethodField()
    empresa = serializers.SerializerMethodField()

    class Meta:
        model = Aprendiz
        fields = '__all__'

    def get_planeacion(self, obj):
        planeacion = Planeacion.objects.filter(aprendiz=obj).first()  # Cambio aquí
        serializer = PlaneacionSerializer(planeacion, many=False)
        return serializer.data if planeacion else None

    def get_seguimiento(self, obj):
        seguimiento = Seguimiento.objects.filter(aprendiz=obj).first()  # Cambio aquí
        serializer = SeguimientoSerializer(seguimiento, many=False)
        return serializer.data if seguimiento else None

    def get_evaluacion(self, obj):
        evaluacion = Evaluacion.objects.filter(aprendiz=obj).first()  # Cambio aquí
        serializer = EvaluacionSerializer(evaluacion, many=False)
        return serializer.data if evaluacion else None
    
    def get_ficha(self, obj):
        ficha = Ficha.objects.filter(aprendiz=obj).first()  # Cambio aquí
        serializer = FichaSerializer(ficha, many=False)
        return serializer.data if ficha else None
    
    def get_empresa(self, obj):
        empresa = Empresa.objects.filter(aprendiz=obj).first()  # Cambio aquí
        serializer = EmpresaSerializer(empresa, many=False)
        return serializer.data if empresa else None
