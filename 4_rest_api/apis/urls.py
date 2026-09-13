from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apis.views.v1.student import StudentViewSet
from apis.views.v1.teacher import TeacherViewSet
from apis.views.v1.school import SchoolViewSet
from apis.views.v1.classroom import ClassroomViewSet

router = DefaultRouter()
router.register('students', StudentViewSet, basename='student')
router.register('teachers', TeacherViewSet, basename='teacher')
router.register('schools', SchoolViewSet, basename='school')
router.register('classrooms', ClassroomViewSet, basename='classroom')

api_v1_urls = (router.urls, 'v1')

urlpatterns = [
    path('v1/', include(api_v1_urls))
]
