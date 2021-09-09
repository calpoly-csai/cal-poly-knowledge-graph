# flask_graphene_mongo/schema.py
import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import Location as LocationModel
from models import Textbook as TextbookModel
from models import Professor as ProfessorModel
from models import CourseMetrics as CourseMetricsModel
from models import Course as CourseModel

class Location(MongoengineObjectType):

    class Meta:
        model = LocationModel
        interfaces = (Node,)

class Textbook(MongoengineObjectType):

    class Meta:
        model = TextbookModel
        interfaces = (Node,)

class Professor(MongoengineObjectType):

    class Meta:
        model = ProfessorModel
        interfaces = (Node,)

class CourseMetrics(MongoengineObjectType):

    class Meta:
        model = CourseMetricsModel
        interfaces = (Node,)

class Course(MongoengineObjectType):

    class Meta:
        model = CourseModel
        interfaces = (Node,)

class Query(graphene.ObjectType):
    node = Node.Field()
    location = MongoengineConnectionField(Location, search = graphene.String())
    textbook = MongoengineConnectionField(Textbook, search = graphene.String())
    professor = MongoengineConnectionField(Professor, search = graphene.String())
    course_metrics = MongoengineConnectionField(CourseMetrics, search = graphene.String())
    course = MongoengineConnectionField(Course, search = graphene.String())

    def resolve(self, info, search=None, **kwargs):
        if search:
            filter = (
                Q(name=search)
            )
            return Link.objects.filter(filter)
        return Link.objects.all()

schema = graphene.Schema(query=Query, types=[Location, Textbook, Professor, CourseMetrics, Course])