# flask_graphene_mongo/models.py
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    StringField, ReferenceField, EmbeddedDocumentField, ListField 
)

class Location(Document):
    meta = {'collection': 'location'}
    name = StringField()
    building_name = StringField(default = "UNSPECIFIED")
    room_number = StringField(default = "UNSPECIFIED")
    latitude = StringField()
    longitude = StringField()
    professor = ReferenceField("Professor")
    textbook = ReferenceField("Textbook")
    courses = ListField(ReferenceField("Course"))

class Textbook(Document):
    meta = {'collection': 'textbook'}
    name = StringField()
    author = StringField()
    isbn = StringField()
    professor = ReferenceField("Professor")
    location = ReferenceField("Location")
    courses = ListField(ReferenceField("Course"))

class Professor(Document):
    meta = {'collection': 'professor'}
    name = StringField()
    location = ReferenceField("Location")
    textbook = ReferenceField("Textbook")
    course = ReferenceField("Course")

class CourseMetrics(EmbeddedDocument):
    meta = {'collection': 'coursemetrics'}
    homework_hours_per_week = StringField()
    average_pass_rate = StringField()

class Course(Document):
    meta = {'collection': 'course'}
    name = StringField()
    metrics = EmbeddedDocumentField("CourseMetrics", required = True)
    professor = ReferenceField("Professor", required = True)
    textbook = ReferenceField("Textbook", required = True)
    course_location = ReferenceField("Location", required = True)