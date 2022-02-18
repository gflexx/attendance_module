from django.urls import path

from .views import *

urlpatterns = [
    path('register/student', student_registration),
    path('register/lecturer', lecturer_registration),

    path('login', login),
    path('logout', logout),

    path('profile', profile_view),
    path('get/units', get_units),
    path('get/classmates', get_classmates),
]