# Create your views here.
from yaksh.models import Course
from .serializers import CourseSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
class CourseList(APIView):
    permission_classes=[AllowAny]
    def get(self,request):
        data=Course.objects.all()
        serializer=CourseSerializer(data,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=CourseSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer._validated_data)
        return Response(serializer.errors)    

