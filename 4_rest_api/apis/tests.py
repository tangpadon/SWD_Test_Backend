from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APIClient

from apis.models import School, Classroom, Teacher, Student


class SchoolAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.school = School.objects.create(
            name='รร.สาธิต', abbreviation='SDT', address='ถ.พระราม'
        )

    def test_create_school(self):
        res = self.client.post('/api/v1/schools/', {
            'name': 'รร.ใหม่', 'abbreviation': 'NEW', 'address': 'ถ.เพชร'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], 'รร.ใหม่')

    def test_list_schools(self):
        res = self.client.get('/api/v1/schools/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_filter_school_by_name(self):
        res = self.client.get('/api/v1/schools/', {'name': 'รร.สาธิต'})
        self.assertEqual(len(res.data), 1)
        res = self.client.get('/api/v1/schools/', {'name': 'ไม่มีอยู่'})
        self.assertEqual(len(res.data), 0)

    def test_school_detail_with_counts(self):
        classroom = Classroom.objects.create(
            school=self.school, grade='ม.4', room='4/2'
        )
        teacher = Teacher.objects.create(
            firstname='สมชาย', lastname='ใจดี', gender='M'
        )
        teacher.classrooms.add(classroom)
        Student.objects.create(
            firstname='น้อง', lastname='เล็ก', gender='F',
            classroom=classroom
        )

        res = self.client.get(f'/api/v1/schools/{self.school.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['classroom_count'], 1)
        self.assertEqual(res.data['teacher_count'], 1)
        self.assertEqual(res.data['student_count'], 1)

    def test_update_school(self):
        res = self.client.patch(
            f'/api/v1/schools/{self.school.id}/',
            {'address': 'ถ.ใหม่'}, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.school.refresh_from_db()
        self.assertEqual(self.school.address, 'ถ.ใหม่')

    def test_delete_school(self):
        res = self.client.delete(f'/api/v1/schools/{self.school.id}/', HTTP_ACCEPT='application/json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        res = self.client.get(f'/api/v1/schools/{self.school.id}/')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class ClassroomAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.school_a = School.objects.create(
            name='รร.A', abbreviation='A', address='addr A'
        )
        self.school_b = School.objects.create(
            name='รร.B', abbreviation='B', address='addr B'
        )
        self.classroom = Classroom.objects.create(
            school=self.school_a, grade='ป.1', room='1/1'
        )

    def test_create_classroom(self):
        res = self.client.post('/api/v1/classrooms/', {
            'school': self.school_a.id, 'grade': 'ป.2', 'room': '2/1'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['grade'], 'ป.2')

    def test_filter_by_school(self):
        res = self.client.get(
            '/api/v1/classrooms/', {'school': self.school_a.id}
        )
        self.assertEqual(len(res.data), 1)
        res = self.client.get(
            '/api/v1/classrooms/', {'school': self.school_b.id}
        )
        self.assertEqual(len(res.data), 0)

    def test_detail_shows_teachers_and_students(self):
        teacher = Teacher.objects.create(
            firstname='ครูคนแรก', lastname='ใจงาม', gender='F'
        )
        teacher.classrooms.add(self.classroom)
        Student.objects.create(
            firstname='น้องเล็ก', lastname='สดใส', gender='M',
            classroom=self.classroom
        )

        res = self.client.get(f'/api/v1/classrooms/{self.classroom.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['teachers'][0]['firstname'], 'ครูคนแรก')
        self.assertEqual(res.data['students'][0]['firstname'], 'น้องเล็ก')

    def test_classroom_has_many_teachers(self):
        teacher_a = Teacher.objects.create(
            firstname='ครูคนที่หนึ่ง', lastname='ใจดี', gender='M'
        )
        teacher_a.classrooms.add(self.classroom)
        teacher_b = Teacher.objects.create(
            firstname='ครูคนที่สอง', lastname='ใจดี', gender='M'
        )
        teacher_b.classrooms.add(self.classroom)
        res = self.client.get(f'/api/v1/classrooms/{self.classroom.id}/')
        self.assertEqual(len(res.data['teachers']), 2)

    def test_delete_classroom(self):
        res = self.client.delete(f'/api/v1/classrooms/{self.classroom.id}/', HTTP_ACCEPT='application/json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class TeacherAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.school = School.objects.create(
            name='รร.สาธิต', abbreviation='SDT', address='addr'
        )
        self.classroom = Classroom.objects.create(
            school=self.school, grade='ม.4', room='4/2'
        )
        self.teacher = Teacher.objects.create(
            firstname='สมชาย', lastname='ใจดี', gender='M'
        )
        self.teacher.classrooms.add(self.classroom)

    def test_create_teacher(self):
        res = self.client.post('/api/v1/teachers/', {
            'firstname': 'สมหญิง', 'lastname': 'สวยงาม',
            'gender': 'F', 'classrooms': []
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['gender'], 'F')
        self.assertEqual(
            Teacher.objects.filter(firstname='สมหญิง').count(), 1
        )

    def test_invalid_gender_rejected(self):
        res = self.client.post('/api/v1/teachers/', {
            'firstname': 'X', 'lastname': 'Y',
            'gender': 'X', 'classrooms': []
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_teacher(self):
        res = self.client.get(
            '/api/v1/teachers/', {'firstname': 'สมชาย'}
        )
        self.assertEqual(len(res.data), 1)
        res = self.client.get('/api/v1/teachers/', {'gender': 'M'})
        self.assertEqual(len(res.data), 1)
        res = self.client.get(
            '/api/v1/teachers/', {'classrooms': self.classroom.id}
        )
        self.assertEqual(len(res.data), 1)
        res = self.client.get(
            '/api/v1/teachers/',
            {'classrooms__school': self.school.id}
        )
        self.assertEqual(len(res.data), 1)
        res = self.client.get(
            '/api/v1/teachers/', {'lastname': 'ไม่มีตัวตน'}
        )
        self.assertEqual(len(res.data), 0)

    def test_detail_shows_classrooms(self):
        res = self.client.get(f'/api/v1/teachers/{self.teacher.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['classrooms'][0]['grade'], 'ม.4')

    def test_teacher_can_be_in_multiple_classrooms(self):
        another = Classroom.objects.create(
            school=self.school, grade='ม.5', room='5/1'
        )
        self.teacher.classrooms.add(another)
        res = self.client.get(f'/api/v1/teachers/{self.teacher.id}/')
        self.assertEqual(len(res.data['classrooms']), 2)

    def test_update_teacher(self):
        res = self.client.patch(
            f'/api/v1/teachers/{self.teacher.id}/',
            {'lastname': 'ใจดีมาก'}, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.lastname, 'ใจดีมาก')

    def test_delete_teacher(self):
        res = self.client.delete(f'/api/v1/teachers/{self.teacher.id}/', HTTP_ACCEPT='application/json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class StudentAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        school = School.objects.create(
            name='รร.สาธิต', abbreviation='SDT', address='addr'
        )
        self.classroom = Classroom.objects.create(
            school=school, grade='ป.1', room='1/1'
        )
        self.student = Student.objects.create(
            firstname='น้อง', lastname='เล็ก', gender='F',
            classroom=self.classroom
        )

    def test_create_student(self):
        res = self.client.post('/api/v1/students/', {
            'firstname': 'น้องใหญ่', 'lastname': 'โต',
            'gender': 'M', 'classroom': self.classroom.id
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['classroom'], self.classroom.id)

    def test_filter_student(self):
        res = self.client.get(
            '/api/v1/students/', {'classroom': self.classroom.id}
        )
        self.assertEqual(len(res.data), 1)
        res = self.client.get('/api/v1/students/', {'gender': 'M'})
        self.assertEqual(len(res.data), 0)
        res = self.client.get(
            '/api/v1/students/',
            {'classroom__school': self.classroom.school.id}
        )
        self.assertEqual(len(res.data), 1)

    def test_detail_shows_classroom(self):
        res = self.client.get(f'/api/v1/students/{self.student.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['classroom'], self.classroom.id)

    def test_student_belongs_to_exactly_one_classroom(self):
        another = Classroom.objects.create(
            school=self.classroom.school, grade='ป.2', room='2/1'
        )
        res = self.client.patch(
            f'/api/v1/students/{self.student.id}/',
            {'classroom': another.id}, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.classroom.id, another.id)

    def test_delete_student(self):
        res = self.client.delete(f'/api/v1/students/{self.student.id}/', HTTP_ACCEPT='application/json')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)