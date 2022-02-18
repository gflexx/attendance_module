# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.conf import settings
# from django.db import models

# from users.models import User
# from users.utils import course_code_extractor

# class Faculty(models.Model):
#     name = models.CharField(max_length=99)
#     dean = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         null=True, 
#         on_delete=models.SET_NULL,
#         related_name='fuculty_dean'
#     )

#     class Meta:
#         db_table = 'faculties'
#         verbose_name_plural = 'faculties'

#     def __str__(self):
#         return self.name

# # school model
# class School(models.Model):
#     name = models.CharField(max_length=99)
#     faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
#     director = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         null=True, 
#         on_delete=models.SET_NULL,
#         related_name='school_director'
#     )
#     lecturers = models.ManyToManyField(
#         settings.AUTH_USER_MODEL, 
#         blank=True
#     )

#     def __str__(self):
#         return self.name

# # deparment model
# class Deparment(models.Model):
#     name = models.CharField(max_length=99)
#     school = models.ForeignKey(School, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name

# # course model
# class Course(models.Model):
#     name = models.CharField(max_length=99)
#     department = models.ForeignKey(
#         Deparment, 
#         on_delete=models.CASCADE,
#         blank=True,
#         null=True,
#     )
#     code = models.CharField(max_length=9)
#     students = models.ManyToManyField(
#         settings.AUTH_USER_MODEL,
#         blank=True,
#         related_name='course_students',
#     )
         
#     def __str__(self):
#         return self.name

# # unit model
# class Unit(models.Model):
#     title = models.CharField(max_length=99)
#     lecturer = models.ManyToManyField(
#         settings.AUTH_USER_MODEL,
#         blank=True,
#         related_name='unit_lecturer',
#     )
#     course = models.ManyToManyField(
#         Course,
#         blank=True, 
#         related_name='unit_course',
#     )
#     code = models.CharField(max_length=9)

#     def __str__(self):
#         return self.code

# # room model
# class Room(models.Model):
#     name = models.CharField(max_length=18)

#     def __str__(self):
#         return self.name

# # lecture model
# class Lecture(models.Model):
#     lecturer = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         null=True,
#         on_delete=models.SET_NULL,
#     )
#     room = models.ForeignKey(
#         Room, 
#         on_delete=models.CASCADE
#     )
#     unit = models.ForeignKey(
#         Unit, 
#         on_delete=models.CASCADE
#     )
#     time = models.DateTimeField()

#     def __str__(self):
#         return '{} - {}'.format(self.unit, self.room)
        