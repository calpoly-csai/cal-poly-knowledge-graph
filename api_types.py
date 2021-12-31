"""
Classes that bind the MongoEngine models with the Graphene GraphQL API
"""

import models
from graphene.relay import Node
from graphene_mongo import MongoengineObjectType, converter
import graphene


class College(MongoengineObjectType):
    """
    A sub-college of Cal Poly. E.g. College of Engineering
    """

    class Meta:
        model = models.College
        interfaces = (Node,)


class Department(MongoengineObjectType):
    """
    An area of study within a college. E.g. Computer Science Department
    """

    class Meta:
        model = models.Department
        interfaces = (Node,)


class Program(MongoengineObjectType):
    """
    A field of study taken up by a student. E.g. majoring in Computer Science
    """

    class Meta:
        model = models.Program
        interfaces = (Node,)


class Room(MongoengineObjectType):
    """
    A publically accessible room inside a campus building.
    """

    class Meta:
        model = models.Room
        interfaces = (Node,)


class Club(MongoengineObjectType):
    """
    A Cal Poly student organization
    """

    class Meta:
        model = models.Club
        interfaces = (Node,)


class Professor(MongoengineObjectType):
    """
    A person who teaches a class at Cal Poly
    """

    class Meta:
        model = models.Professor
        interfaces = (Node,)


class Course(MongoengineObjectType):
    """
    An abstract course that is taught at Cal Poly. For specific sections/classes taught in a specific quarter, see Section
    """

    class Meta:
        model = models.Course
        interfaces = (Node,)
