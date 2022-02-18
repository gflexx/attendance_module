from datetime import datetime, timedelta
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response

from py2neo import NodeMatcher, RelationshipMatcher

from neo4j import *
from .serializers import *
from users.utils import course_year_extractor

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication,])
def add_lecture(request):
    user = request.user
    serializer = AddLectureSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        lecture = serializer.save()
        data['message'] = 'Lecture Added'
        data['unit'] = lecture['unit']
        data['lecturer'] = lecture['lecturer']
        data['time'] = lecture['time']
        data['year'] = lecture['year']
    else:
        data = serializer.errors
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication,])
def get_lectures(request):
    data = {}
    node_matcher = NodeMatcher(graph)
    lectures = node_matcher.match('LectureNode')
    cont = []
    for lecture in lectures:
        cont.append(
            dict({'time':list(lecture.items())[1][1], 
            'name':list(lecture.items())[0][1],
            'year':list(lecture.items())[2][1]
        }))
    data['lectures'] = cont
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication,])
def get_lectures(request):
    data = {}
    user = request.user
    if user.is_student:
        reg_num = user.reg_number
        year = course_year_extractor(reg_num)
        student = StudentNode.match(graph, reg_num).first()
        crse = []
        units = []
        lectures = []
        # get course associated with student
        for course in student.student_of:
            crse.append(course.name)

            # get units associated with course
            for unit in course.units:
                units.append(dict(
                    {
                        'name': unit.name,
                        'code': unit.code
                    }
                ))

                # get lectures associated with unit
                for lecture in unit.lecture:
                    if lecture.year == year:
                        lectures.append(dict(
                            {
                                'name': lecture.name, 
                                'time': lecture.time, 
                                'lecturer': str([lec.full_name for lec in lecture.lecturer][0])
                            }
                        ))

        data['full_name'] = student.full_name
        data['reg_number'] = student.reg_number
        data['course'] = crse
        data['units'] = units
        data['lectures'] = lectures
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication,])
def attend_lecture(request):
    data = {}
    user = request.user
    if user.is_student:
        reg_num = user.reg_number
        year = course_year_extractor(reg_num)
        student = StudentNode.match(graph, reg_num).first()

        # get time now
        time_now = datetime.now()

        # perform query to get lectures
        query = "\
            MATCH (s:StudentNode)-[:STUDENT_OF]-(course)-[:UNITS_IN]-(units)-[:LECTURE]-(lectures)\
            -[:ATTENDANCE]-(attend)\
            WHERE(s.reg_number='%s') RETURN DISTINCT lectures, attend" % reg_num
        units = list(graph.run(query))

        lectures = []
        for unit in units:
            # get time of lecture
            # convert from string into date time 
            formated_time = datetime.strptime(list(list(unit)[0].values())[1], '%Y/%m/%d %H:%M')

            # check if lecture is alocated for student year
            if list(list(unit)[0].values())[2] == year:

                # check if time delta, difference is within one hour
                time_difference = time_now - formated_time
                if time_difference.seconds <= 5000 and time_difference.seconds > 0:
                    lectures.append(dict({'lecture': list(unit)[0], 'attendance': list(unit)[1]}))
                    print(list(unit)[1].relationships)
        print(lectures)
        data['full_name'] = student.full_name
        data['reg_number'] = student.reg_number
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication,])
def get_attendace(request):
    data = {}
    node_matcher = NodeMatcher(graph)
    lectures = node_matcher.match('LectureNode')
    cont = []
    for lecture in lectures:
        cont.append(dict({'code':list(lecture.items())[1][1], 'name':list(lecture.items())[0][1]}))
    data['courses'] = cont
    return Response(data)