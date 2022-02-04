from rest_framework import serializers
from .models import Bigyo

class BigyoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bigyo
        fields = '__all__'
