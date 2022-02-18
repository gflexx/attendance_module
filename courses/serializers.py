from rest_framework import serializers

from neo4j import *

class FucultySerializer(serializers.BaseSerializer):
    # set fuculty name field
    name = serializers.CharField(
        read_only=True,
    )

    # set dean field
    dean = serializers.CharField(
        read_only=True,
    )

    # serializer field and extra field proerties
    class Meta:
        fields = ('name', 'dean',)
        extra_kwargs = {
            'name': {'required', True},
            'dean': {'required', True},
        }

    # vailidate incoming data
    def to_internal_value(self, data):
        # require name
        name = data.get('name')
        if not name:
            raise serializers.ValidationError({
                'name': 'Fuculty name is required.'
            })

        dean = data.get('dean')
        dean = dean.upper()
        # check if dean exists
        lec = LecturerNode.match(graph, dean).first()
        if not lec:
            raise serializers.ValidationError({
                'dean': 'Dean staff id not yet registered.'
            })

        # require dean
        if not dean:
            raise serializers.ValidationError({
                'dean': 'Dean staff id is required.'
            })

        return {
            'name': name.upper(),
            'dean': lec
        }
    
    # save nodes and relationships
    def save(self):
        lec = self.validated_data['dean']
        name = self.validated_data['name']
        fuculty = FacultyNode(
            name = name
        )
        fuculty.dean.add(lec)
        graph.create(fuculty)
        lec.dean_in.add(fuculty)
        graph.push(lec)
        data = {
            'name': fuculty.name,
            'dean': lec.full_name
        }
        return data

class SchoolSerializer(serializers.BaseSerializer):
    # set school name field
    name = serializers.CharField(
        read_only=True,
    )

    # set director field
    director = serializers.CharField(
        read_only=True,
    )

    # set fuculty field
    fuculty = serializers.CharField(
        read_only=True,
    )

    # serializer field and extra field proerties
    class Meta:
        fields = ('name', 'director', 'fuculty')
        extra_kwargs = {
            'name': {'required', True},
            'director': {'required', True},
            'fuculty': {'required', True},
        }

    # validate incoming data
    def to_internal_value(self, data):
        # require name
        name = data.get('name')
        if not name:
            raise serializers.ValidationError({
                'name': 'School name is required.'
            })

        director = data.get('director')
        director = director.upper()
        # check if director exists
        lec = LecturerNode.match(graph, director).first()
        if not lec:
            raise serializers.ValidationError({
                'director': 'Director staff id not yet registered.'
            })

        # require director
        if not director:
            raise serializers.ValidationError({
                'director': 'Director staff id is required.'
            })

        fuculty = data.get('fuculty')
        fuculty = fuculty.upper()
        # require fuculty
        if not fuculty:
            raise serializers.ValidationError({
                'fuculty': 'Fuculty is required.'
            })

        # check if school exists
        fclt = FacultyNode.match(graph, fuculty).first()
        if not fclt:
            raise serializers.ValidationError({
                'fuculty': 'Fuculty entered is not yet registered.'
            })
        
        return {
            'name': name.upper(),
            'director': lec,
            'fuculty': fclt,
        }
    
    # save nodes and relationships
    def save(self):
        lec = self.validated_data['director']
        name = self.validated_data['name']
        fuculty = self.validated_data['fuculty']
        school = SchoolNode(
            name = name
        )
        school.director.add(lec)
        school.fuculty.add(fuculty)
        graph.create(school)
        fuculty.schools.add(school)
        graph.push(fuculty)
        lec.director_of.add(school)
        graph.push(lec)
        data = {
            'name': school.name,
            'director': lec.full_name
        }
        return data

class DepartmentSerializer(serializers.BaseSerializer):
    # set department name field
    name = serializers.CharField(
        read_only=True,
    )

    # set school field
    school = serializers.CharField(
        read_only=True,
    )

    # serializer field and extra field proerties
    class Meta:
        fields = ('name', 'school',)
        extra_kwargs = {
            'name': {'required', True},
            'school': {'required', True},
        }

    def to_internal_value(self, data):
        name = data.get('name')
        if not name:
            raise serializers.ValidationError({
                'name': 'Department name is required.'
            })

        school = data.get('school')
        school = school.upper()
        # require school
        if not school:
            raise serializers.ValidationError({
                'school': 'School name is required.'
            })

        # check if school exists
        school_ = SchoolNode.match(graph, school).first()
        if not school_:
            raise serializers.ValidationError({
                'school': 'School name not yet registered.'
            })

        return {
            'name': name.upper(),
            'school': school_
        }

    # save nodes and relationships
    def save(self):
        school = self.validated_data['school']
        name = self.validated_data['name']
        dept = DepartmentNode(
            name = name
        )
        dept.school.add(school)
        graph.create(dept)
        school.departments.add(dept)
        graph.push(school)
        data = {
            'name': dept.name,
            'school': school.name
        }
        return data
       

class CourseSerializer(serializers.BaseSerializer):
    # set course name field
    name = serializers.CharField(
        read_only=True,
    )

    # set course code field
    code = serializers.CharField(
        read_only=True,
    )

    # set department field
    department = serializers.CharField(
        read_only=True,
    )

    # serializer field and extra field proerties
    class Meta:
        fields = ('name', 'code', 'department')
        extra_kwargs = {
            'name': {'required', True},
            'code': {'required', True},
            'department': {'required', True},
        }

    def to_internal_value(self, data):
        name = data.get('name')
        if not name:
            raise serializers.ValidationError({
                'name': 'Course name is required.'
            })

        code = data.get('code')
        if not code:
            raise serializers.ValidationError({
                'code': 'Course is required.'
            })

        department = data.get('department')
        department = department.upper()
        if not department:
            raise serializers.ValidationError({
                'name': 'Department name is required.'
            })

        dept = DepartmentNode.match(graph, department).first()
        if not dept:
            raise serializers.ValidationError({
                'name': 'Department is not yet registered.'
            })

        return {
            'name': name.upper(),
            'code': code.upper(),
            'department': dept
        }

    # save nodes and relationships
    def save(self):
        code = self.validated_data['code']
        name = self.validated_data['name']
        department = self.validated_data['department']
        course = CourseNode(
            name = name,
            code = code,
        )
        course.department.add(department)
        graph.create(course)
        department.courses.add(course)
        graph.push(department)
        data = {
            'name': course.name,
            'code': course.code,
            'department': department.name,
        }
        return data

class UnitSerializer(serializers.BaseSerializer):
    # set unit name field
    name = serializers.CharField(
        read_only=True,
    )

    # set unit code field
    code = serializers.CharField(
        read_only=True,
    )

    # set course field
    course = serializers.CharField(
        read_only=True,
    )

    # serializer field and extra field proerties
    class Meta:
        fields = ('name', 'code', 'course')
        extra_kwargs = {
            'name': {'required', True},
            'code': {'required', True},
            'course': {'required', True},
        }

    def to_internal_value(self, data):
        name = data.get('name')
        if not name:
            raise serializers.ValidationError({
                'name': 'Unit name is required.'
            })

        code = data.get('code')
        if not code:
            raise serializers.ValidationError({
                'code': 'Unit code is required.'
            })

        course = data.get('course')
        course = course.upper()
        if not course:
            raise serializers.ValidationError({
                'name': 'Course code is required.'
            })

        crs = CourseNode.match(graph, course).first()
        if not crs:
            raise serializers.ValidationError({
                'course': 'Course code is not yet registered.'
            })

        return {
            'name': name.upper(),
            'code': code.upper(),
            'course': crs
        }

    # save nodes and relationships
    def save(self):
        code = self.validated_data['code']
        name = self.validated_data['name']
        course = self.validated_data['course']
        unit = UnitNode(
            name = name,
            code = code,
        )
        unit.course.add(course)
        graph.create(unit)
        course.units.add(unit)
        graph.push(course)
        data = {
            'name': unit.name,
            'code': unit.code,
            'course': course.name,
        }
        return data    
        