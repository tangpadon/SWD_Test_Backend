from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from apis.models import Classroom
from apis.serializers import ClassroomSerializer
from apis.filters import ClassroomFilter

class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    filterset_class = ClassroomFilter
    permission_classes = [AllowAny]