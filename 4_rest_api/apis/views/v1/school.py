from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from apis.models import School
from apis.serializers import SchoolSerializer
from apis.filters import SchoolFilter


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    filterset_class = SchoolFilter
    permission_classes = [AllowAny]