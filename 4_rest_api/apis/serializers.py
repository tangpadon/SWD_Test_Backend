from rest_framework import serializers


# code here
from apis.models import School, Classroom, Teacher, Student

class SchoolSerializer(serializers.ModelSerializer):
    classroom_count = serializers.SerializerMethodField()
    teacher_count = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = ['id', 'name', 'abbreviation', 'address', 'classroom_count', 'teacher_count', 'student_count']
        fields = '__all__'

    def get_classroom_count(self, obj):
        return obj.classrooms.count()
    
    def get_teacher_count(self, obj):
        return Teacher.objects.filter(classrooms__school=obj).distinct().count()
    
    def get_student_count(self, obj):
        return Student.objects.filter(classroom__school=obj).count()

class StudentSerializer(serializers.ModelSerializer):
    classroom = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())

    class Meta:
        model = Student
        fields = '__all__'

class ClassroomSerializer(serializers.ModelSerializer):
    teachers = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), many=True)

    class Meta:
        model = Classroom
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['teachers'] = TeacherSerializer(instance.teachers, many=True).data
        data['students'] = StudentSerializer(instance.students, many=True).data
        return data

class TeacherSerializer(serializers.ModelSerializer):
    classrooms = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all(), many=True)

    class Meta:
        model = Teacher
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['classrooms'] = ClassroomSerializer(instance.classrooms, many=True).data
        return data