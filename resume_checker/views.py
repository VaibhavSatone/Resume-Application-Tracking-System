from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import JobDescriptionSerializer,Jobdescription,ResumeSerializer,Resume
from .analyzer import process_resume

# Create your views here.
class JobDescriptionAPI(APIView):
    def get(self,request):
        queryset =Jobdescription.objects.all()
        serializer=JobDescriptionSerializer(queryset, many= True)
        return Response({
            'status':True,
            'data':serializer.data
        })
class AnalyzeResumeAPI(APIView):
    def post(self,request):
        try:
            data=request.data
            if not data.get('job_description'):
                return Response({'status':False,
                                 'message':'job_description is required',
                                 'data':{}}) 
            serializer=ResumeSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'status':False,
                    'message':'errors',
                    'data':serializer.errors
                })
            serializer.save()
            _data=serializer.data
            resume_instance=Resume.objects.get(id=_data['id'])
            resume_path=resume_instance.resume.path
            result=process_resume(resume_path,Jobdescription.objects.get(id=data.get('job_description')).job_description)
            return Response({'status':True,
                                 'message':'result analyzed',
                                 'data':result}) 
        except Exception as e:
            return Response({'data':False})