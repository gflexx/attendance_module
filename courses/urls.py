from django.urls import path

from .views import *

urlpatterns = [
    path('api/add/fuculty', add_fuculty),
    path('api/add/school', add_school),
    path('api/add/department', add_department),
    path('api/add/course', add_course),
    path('api/add/unit', add_unit),
    path('api/get/all/students', get_all_students),
    path('api/get/all/lecturers', get_all_lecturers),
    path('api/get/all/courses', get_all_courses),
    path('api/get/all/units', get_all_units),
]