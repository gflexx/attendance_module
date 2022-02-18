from django.db.models import fields
from rest_framework import serializers

from py2neo import NodeMatcher

from .models import User
from .utils import course_code_extractor
from neo4j import *

class RegistrationSerializer(serializers.ModelSerializer):

    # set confirm password field
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    # set lecturer registration field
    lecturer_registration = serializers.IntegerField(
        write_only=True,
        required=False,
        default=0
    )

    # set student registration field
    student_registration = serializers.IntegerField(
        write_only=True,
        required=False,
        default=0
    )

    # serializer model, field and extra field proerties
    class Meta:
        model = User
        fields = ('email', 'image', 'full_name', 'staff_id', 'reg_number', 'lecturer_registration', 'student_registration', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True},
            'lecturer_registration': {'write_only': True},
            'student_registration': {'write_only': True},
        }
    
    def save(self):
        user = User(
            email=self.validated_data['email'],
            full_name=self.validated_data['full_name'],
        )

        # if student_registration is set, register student
        student_registration = self.validated_data['student_registration']
        if student_registration == 1:
            reg_number = self.validated_data['reg_number']

            # raise error if reg number not set
            if reg_number is None:
                raise serializers.ValidationError(
                    {'Registration Number': 'Your registration number is required!'}
                )

            # check if reg number has right course code
            course_code = course_code_extractor(reg_number)

            node_matcher = NodeMatcher(graph)

            course = node_matcher.match('CourseNode').where(code=course_code).first()

            # register student if code is correct
            if course:
                # save reg number to user
                user.reg_number = reg_number.upper()

            else:
                raise serializers.ValidationError(
                    {'Registration Number': 'Incorrect course code contact administrator!'}
                )
            
        # if lecturer_registration is set, register lecturer
        lecturer_registration = self.validated_data['lecturer_registration']
        if lecturer_registration == 1:
            staff_id = self.validated_data['staff_id']

            # raise error if staff id not set
            if staff_id is None:
                raise serializers.ValidationError(
                    {'Staff ID': 'Your staff id is required!'}
                )
            
            user.staff_id = staff_id.upper()

        # check if passwords match, return error if not
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords must match!'}
            )

        # set password and save user
        user.set_password(password)
        user.save()
        return user