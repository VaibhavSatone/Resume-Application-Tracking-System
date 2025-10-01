from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import JobDescriptionSerializer,Jobdescription

# Create your views here.
class JobDescriptionAPI(APIView):
    def get(self,request):
        queryset =Jobdescription.objects.all()
        serializer=JobDescriptionSerializer(queryset, many= True)
        return Response({
            'status':True,
            'data':serializer.data
        })

