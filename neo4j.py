import os, json
from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo

# open config file
with open('config.json') as config_file:
    config = json.load(config_file)

# connect to graph database
graph_url = config['db_url']
graph_user = config['db_user']
db_password = config['db_password']
graph = Graph(host='localhost', user=graph_user, password=db_password)

# neo4j models
# lecturer node model
class LecturerNode(GraphObject):
    __primarykey__ = 'staff_id'

    full_name = Property()
    staff_id = Property()

    dean_in = RelatedTo('FacultyNode', 'DEAN_IN')
    director_of = RelatedTo('SchoolNode', 'DIRECTOR_OF')
    lecture = RelatedTo('LectureNode', 'HAS_LECTURE')
    unit = RelatedTo('UnitNode', 'TEACHES_UNIT')

# student model
class StudentNode(GraphObject):
    __primarykey__ = 'reg_number'

    full_name = Property()
    reg_number = Property()

    student_of = RelatedTo('CourseNode', 'STUDENT_OF')

# fuculty model
class FacultyNode(GraphObject):
    __primarykey__ = 'name'

    name = Property()

    dean = RelatedTo(LecturerNode)
    schools = RelatedTo('SchoolNode', 'SCHOOL')

# school model
class SchoolNode(GraphObject):
    __primarykey__ = 'name'

    name = Property()

    fuculty = RelatedTo('FacultyNode', 'FUCULTY')
    director = RelatedTo(LecturerNode)
    departments = RelatedTo('DepartmentNode', 'DEPARTMENTS_IN')

# department model
class DepartmentNode(GraphObject):
    __primarykey__ = 'name'

    name = Property()

    school = RelatedTo(SchoolNode)
    courses = RelatedTo('CourseNode', 'COURSES_IN')

# course model
class CourseNode(GraphObject):
    __primarykey__ = 'code'

    name = Property()
    code = Property()

    students = RelatedTo(StudentNode)
    department = RelatedTo(DepartmentNode)
    units = RelatedTo('UnitNode', 'UNITS_IN')

# unit model
class UnitNode(GraphObject):
    __primarykey__ = 'code'

    name = Property()
    code = Property()

    course = RelatedTo(CourseNode)
    lecturer = RelatedTo(LecturerNode)
    lecture = RelatedTo('LectureNode')

# lecture model
class LectureNode(GraphObject):
    name = Property()
    time = Property()
    year = Property()

    lecturer = RelatedTo(LecturerNode)
    attendance = RelatedTo('AttendanceNode')
    unit = RelatedTo(UnitNode)

class AttendanceNode(GraphObject):
    time = Property()
    name = Property()

    lecture = RelatedTo('LectureNode')
    students = RelatedTo('StudentNode')
    unit = RelatedTo(UnitNode)
