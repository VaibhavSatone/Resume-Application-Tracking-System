from rest_framework import serializers
from .models import Jobdescription,Resume

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Jobdescription
        fields="__all__"

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Resume
        fields="__all__"