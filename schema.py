# flask_graphene_mongo/schema.py
import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField
from api_types import *


class Query(graphene.ObjectType):
    node = Node.Field()
    college = MongoengineConnectionField(College)
    department = MongoengineConnectionField(Department)
    program = MongoengineConnectionField(Program)
    room = MongoengineConnectionField(Room)
    club = MongoengineConnectionField(Club)
    professor = MongoengineConnectionField(Professor)
    course = MongoengineConnectionField(Course)

schema = graphene.Schema(query=Query)