from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from apis.models import Teacher
from apis.serializers import TeacherSerializer
from apis.filters import TeacherFilter

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filterset_class = TeacherFilter
    permission_classes = [AllowAny]