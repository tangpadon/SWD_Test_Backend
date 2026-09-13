from django.db import models

# Create your models here.
class Gender(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'

class School(models.Model):
    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=20)
    address = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Classroom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classrooms')
    grade = models.CharField(max_length=50)
    room = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.school.name} - {self.grade}/{self.room}"

class Teacher(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    classrooms = models.ManyToManyField(Classroom, related_name='teachers', blank=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Student(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"{self.firstname} {self.lastname}"