from django_filters import FilterSet, filters


# code here
from apis.models import School, Classroom, Teacher, Student

class SchoolFilter(FilterSet):
    class Meta:
        model = School
        fields = {
            'name': ['exact'],
        }

class ClassroomFilter(FilterSet):
    class Meta:
        model = Classroom
        fields = {
            'school': ['exact'],
        }

class TeacherFilter(FilterSet):
    class Meta:
        model = Teacher
        fields = {
            'classrooms__school': ['exact'],
            'classrooms' : ['exact'],
            'firstname': ['exact'],
            'lastname': ['exact'],
            'gender': ['exact'],
        }

class StudentFilter(FilterSet):
    class Meta:
        model = Student
        fields = {
            'classroom__school': ['exact'],
            'classroom' : ['exact'],
            'firstname': ['exact'],
            'lastname': ['exact'],
            'gender': ['exact'],
        }