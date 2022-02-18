from django.urls import path

from .views import *

urlpatterns = [
    path('api/add/lecture', add_lecture),
    path('api/get/all/lectures', get_lectures),
    path('api/lecture/attend', attend_lecture),
    path('api/lectures/get', get_lectures),
    path('api/lectures/get/attendance', get_attendace)
]