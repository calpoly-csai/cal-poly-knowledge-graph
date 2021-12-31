"""
Describes the schema of the GraphQL API
Each property on the Query object is a
"""
import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField
from api_types import *


class Query(graphene.ObjectType):
    """
    The top level structure of the Cal Poly Knowledge Graph API.
    Adding a type below will allow API users to query it directly.

    For example you can query the college field in GraphQL with:
    ```
    query {
        college {...attributes...}
    }
    ```
    """

    node = Node.Field()
    college = MongoengineConnectionField(College)
    department = MongoengineConnectionField(Department)
    program = MongoengineConnectionField(Program)
    room = MongoengineConnectionField(Room)
    club = MongoengineConnectionField(Club)
    professor = MongoengineConnectionField(Professor)
    course = MongoengineConnectionField(Course)


schema = graphene.Schema(query=Query)
