# flask_graphene_mongo/models.py
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    BooleanField,
    DateTimeField,
    DictField,
    EmbeddedDocumentListField,
    EnumField,
    GenericReferenceField,
    IntField,
    StringField,
    ReferenceField,
    EmbeddedDocumentField,
    ListField,
    GeoPointField,
)
from utils import (
    phone_number_regex,
    email_regex,
    ProgramType,
    SectionType,
    Weekday,
    Quarter,
    CourseType,
)


class College(Document):
    """
    A sub-college of Cal Poly. E.g. College of Engineering
    """

    meta = {"collection": "college"}
    name = StringField(required=True)
    description = StringField()
    departments = ListField(ReferenceField("Department"), default=list)


class Department(Document):
    """
    An area of study within a college. E.g. Computer Science Department
    """

    meta = {"collection": "department"}
    name = StringField(required=True)
    description = StringField()
    college = ReferenceField("College")
    programs = ListField(ReferenceField("Program"))
    faculty = ListField(ReferenceField("Professor"))
    courses = ListField(ReferenceField("Course"))
    office = ReferenceField("Room")
    phone_number = StringField(regex=phone_number_regex)
    associated_clubs = ListField(ReferenceField("Club"))


class Program(Document):
    """
    A field of study taken up by a student. E.g. majoring in Computer Science
    """

    meta = {"collection": "program"}
    name = StringField(required=True)
    description = StringField()
    graduate_level = BooleanField(default=False)
    # e.g. major, minor TODO: make this an enum
    type = StringField()
    # TODO: maybe split this out into major support and GE courses
    curriculum = ListField(ReferenceField("Course"))
    department = ReferenceField("Department")


class Building(Document):
    """
    Campus-owned buildings
    """

    meta = {"collection": "building"}
    name = StringField(required=True)
    description = StringField(required=True)
    coordinates = GeoPointField()
    rooms = ListField(ReferenceField("Room"))
    resources = DictField()


class Room(Document):
    """
    A publically accessible room inside a campus building.
    """

    meta = {"collection": "room"}
    building_name = StringField(required=True)
    building = ReferenceField("Building")
    room_number = StringField(required=True, primary_key=True)


class Officer(EmbeddedDocument):
    """
    A leader of a Cal Poly student organization.
    """

    name = StringField(required=True)
    major = StringField()
    position = StringField()
    email = StringField(regex=email_regex)


class Club(Document):
    """
    A Cal Poly student organization
    """

    meta = {"collection": "club"}
    name = StringField(required=True)
    officers = EmbeddedDocumentListField(Officer, required=True)
    email = StringField(regex=email_regex)
    phone = StringField(regex=phone_number_regex)
    social_media: DictField()
    advisor = StringField()


class OfficeHours(EmbeddedDocument):
    """
    A block of time a Professor sets aside to help students.
    """

    start_time = DateTimeField()
    end_time = DateTimeField()
    link = StringField()
    # TODO: Make this an enum Weekday
    weekdays = ListField(field=StringField())


class Professor(Document):
    """
    A person who teaches a class at Cal Poly
    """

    meta = {"collection": "professor"}
    name = StringField(required=True)
    bio = StringField()
    email = StringField(regex=email_regex)
    phone_number = StringField(regex=phone_number_regex)
    sections = ListField(ReferenceField("Section"))
    office = ReferenceField("Room")
    office_hours = EmbeddedDocumentListField(OfficeHours)
    website = StringField()


class Course(Document):
    """
    An abstract course that is taught at Cal Poly. For specific sections/classes taught in a specific quarter, see Section
    """

    meta = {"collection": "course"}
    name = StringField(required=True)
    description = StringField(required=True)
    # TODO: Should this be a list, since CSC 357 is also CPE 357
    course_id = StringField(required=True)
    department = ReferenceField("Department", required=True)
    units = IntField()
    prerequisites = ListField(ReferenceField("Course"))
    sections = ListField(ReferenceField("Section"))
    # TODO: Make Quarter enum
    usually_offered = ListField(StringField())
    # TODO: Make CourseType enum
    course_type = ListField(StringField())


class Section(Document):
    """
    An instance of a course that students attend.
    """

    meta = {"collection": "section"}
    course = ReferenceField("Course")
    section_id = IntField(required=True, primary_key=True)
    # TODO: Make enum type SectionType
    type = StringField()
    asynchronous = BooleanField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    # TODO: Make enum of Weekdays
    weekdays = ListField(StringField())
    room = ReferenceField("Room")
    professors = ListField(ReferenceField("Professor"))
    # TODO: Make enum of Quarter
    quarter = StringField()
