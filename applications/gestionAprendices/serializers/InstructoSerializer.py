from rest_framework import serializers
from ..models.models import InstructorEncargado

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorEncargado
        fields = '__all__'