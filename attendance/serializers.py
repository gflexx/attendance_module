from rest_framework import serializers

from neo4j import *

class AddLectureSerializer(serializers.BaseSerializer):
    # set time field
    time = serializers.CharField(
        read_only=True,
    )

    # set lecturer field
    lecturer = serializers.CharField(
        read_only=True,
    )

    # set unit field
    unit = serializers.CharField(
        read_only=True,
    )

    # set year field
    year = serializers.CharField(
        read_only=True,
    )

    # serializer field and extra field proerties
    class Meta:
        fields = ('time', 'lecturer', 'unit', 'year')
        extra_kwargs = {
            'time': {'required', True},
            'unit': {'required', True},
            'lecturer': {'required', True},
            'year': {'required', True}
        }

    # validate incoming data
    def to_internal_value(self, data):
        unit = data.get('unit')
        unit = unit.upper()

        # require unit
        if not unit:
            raise serializers.ValidationError({
                'unit': 'Unit code is required.'
            })

        # check if unit exists
        unt = UnitNode.match(graph, unit).first()
        if not unt:
            raise serializers.ValidationError({
                'course': 'Unit code is not yet registered.'
            })

        lecturer = data.get('lecturer')
        lecturer = lecturer.upper()

        # require lecturer
        if not lecturer:
            raise serializers.ValidationError({
                'lecturer': 'Lecturer is required.'
            })

        # check if lecturer exists
        lec = LecturerNode.match(graph, lecturer).first()
        if not lec:
            raise serializers.ValidationError({
                'lecturer': 'Lecturer ID is not yet registered.'
            })

        time = data.get('time')
        # require time
        if not time:
            raise serializers.ValidationError({
                'time': 'Unit time is required.'
            })

        year = data.get('year')
        # require year
        if not year:
            raise serializers.ValidationError({
                'year': 'Unit year is required.'
            })

        return {
            'unit': unt,
            'lecturer': lec,
            'time': time,
            'year': year,
        }

    # save nodes and relationships
    def save(self):
        lecturer = self.validated_data['lecturer']
        unit = self.validated_data['unit']
        time = self.validated_data['time']
        year = self.validated_data['year']
        lecture = LectureNode(
            name = unit.code + ' : ' + unit.name,
            time = time,
            year = year
        )
        attendance = AttendanceNode(
            time = time
        )
        attendance.lecture.add(lecture)
        attendance.unit.add(unit)
        lecture.lecturer.add(lecturer)
        lecture.unit.add(unit)
        lecture.attendance.add(attendance)
        graph.create(attendance)
        graph.create(lecture)
        lecturer.lecture.add(lecture)
        graph.push(lecturer)
        lecturer.unit.add(unit)
        graph.push(lecturer)
        unit.lecturer.add(lecturer)
        unit.lecture.add(lecture)
        graph.push(unit)
        data = {
            'unit': unit.code + ' : ' + unit.name,
            'time': lecture.time,
            'lecturer': lecturer.full_name,
            'year': lecture.year
        }
        return data


