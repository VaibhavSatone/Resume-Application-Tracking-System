from rest_framework import serializers
from .models import Jobdescription

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Jobdescription
        fields="__all__"