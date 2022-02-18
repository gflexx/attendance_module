from django.contrib.auth.hashers import check_password
from django.contrib.auth import login

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .serializers import RegistrationSerializer
from .models import User
from .utils import course_year_extractor
from courses.models import *
from neo4j import *

@api_view(['POST'])
def student_registration(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user=user).key
        data['response'] = 'Student registered successfully'
        data['id'] = user.id
        data['reg_number'] = user.reg_number
        data['email'] = user.email
        data['full_name'] = user.full_name
        data['token'] = token
    else:
        data = serializer.errors
    return Response(data)

@api_view(['POST'])
def lecturer_registration(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user=user).key
        data['response'] = 'Lecturer registered successfully'
        data['id'] = user.id
        data['staff_id'] = user.staff_id
        data['email'] = user.email
        data['full_name'] = user.full_name
        data['token'] = token
    else:
        data = serializer.errors
    return Response(data)

@api_view(['POST'])
def login(request):
    data = {}
    email = request.data['email']
    password = request.data['password']

    # check if account exists
    try:
        user = User.objects.get(email=email)
    except BaseException as erorr:
        raise ValidationError(
            {'400': '{}'.format(erorr)}
        )

    # get or create new token
    token = str(Token.objects.get_or_create(user=user)[0])
    data['token'] = token

    # check if password is corresct
    if not check_password(password, user.password):
        raise ValidationError(
            {'message': 'Incorrect credentials'}
        )
    
    if user:
        data['response'] = 'User logged in successfully'
        data['id'] = user.id
        data['email'] = user.email
        data['full_name'] = user.full_name
        return Response(data)
    else:
        raise ValidationError(
            {'400': 'Account doesnt exist'}
        )

@api_view(['POST'])
def logout(request):
    data = {}
    token = request.data['token']

    # check if token exists
    try:
        tkn = Token.objects.get(key=token)
    except BaseException as error:
        raise ValidationError(
            {'400': '{}'.format(error)}
        )

    # get token user for logout delete token
    user = tkn.user
    if user:
        user.auth_token.delete()
        logout(request._request)
        data['response'] = 'User logged out succesfully'
    else:
        raise ValidationError(
            {'400': 'Something went wrong'}
        )
    return Response(data)

# profile view
# require token authentication 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication,])
def profile_view(request):
    data = {}
    user = request.user
    data['full_name'] = user.full_name
    data['email'] = user.email

    # show student details
    if user.is_student:
        reg_number = user.reg_number

        # get student data from neo4j
        student = StudentNode.match(graph, reg_number).first()
        data['reg_number'] = student.reg_number
        courses = []
        for course in student.student_of:
            courses.append(course.name)
        data['course'] = courses
            
    # show lecturer details
    if user.is_lecturer:
        staff_id = user.staff_id

        # get lecturer data from neo4j
        lecturer = LecturerNode.match(graph, staff_id).first()
        data['staff_id'] = lecturer.staff_id

    data['token'] = user.auth_token.key
    
    return Response(data)

# get units
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication,])
def get_units(request):
    data = {}
    user = request.user
    if user.is_student:
        reg_number = user.reg_number
        student = StudentNode.match(graph, reg_number).first()
        data['reg_number'] = student.reg_number
        courses = []
        
        # get courses enrolled
        for course in student.student_of:
            courses.append(course.name)
        data['course'] = courses

        # get units associated with course
        units = []
        for course in student.student_of:
            for unit in course.units:
                units.append(unit.code+ ' : ' + unit.name)

        data['units'] = units

    return Response(data)

# get classmates 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication,])
def get_classmates(request, format=None):
    data = {}
    user = request.user
    reg_number = user.reg_number

    # get year from reg number
    year = course_year_extractor(reg_number)

    student = StudentNode.match(graph, reg_number).first()

    # get courses student is enrolled in
    courses = []
    for course in student.student_of:
        courses.append(course.name)

    data['course'] = courses

    # get students enrolled in course
    students = []
    for course in student.student_of:
        for student in course.students:
            if student.reg_number != reg_number:
                # get year
                std_yr = course_year_extractor(student.reg_number)

                # add student if year is similar
                if std_yr == year:
                    students.append(student.reg_number + ' : ' + student.full_name)

    data['classmates'] = students
    
    return Response(data)
