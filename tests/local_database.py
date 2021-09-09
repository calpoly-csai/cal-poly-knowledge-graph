# flask_graphene_mongo/database.py
from mongoengine import connect

from models import Location, Textbook, Professor, CourseMetrics, Course

connect('graphene-mongo-example', host='mongomock://localhost', alias='default')


def init_db():
    # Create the fixtures
    location1 = Location(name = 'North', building_name = 'Bill Building', room_number = "15", latitude = '15 N', longitude = '30 W')
    location1.save()

    location2 = Location(name = 'South', building_name = 'Tim Building', room_number = "12", latitude = '15 S', longitude = '30 E')
    location2.save()

    textbook1 = Textbook(name = 'Intro to Python Programming', author = "Richard Brand", isbn = "9187434556789")
    textbook1.save()

    textbook2 = Textbook(name = 'Intro to C Programming', author = "Chris Lin", isbn = "4782901283451")
    textbook2.save()

    professor1 = Professor(name = 'Robert Dawson')
    professor1.save()
    
    professor2 = Professor(name = 'Jack Walsh')
    professor2.save()

    course1 = Course(name = 'CSC 357', metrics = CourseMetrics(homework_hours_per_week = "6", average_pass_rate = '60%'), professor = professor1, textbook = textbook1, course_location = location1)
    course1.save()

    course2 = Course(name = 'CSC 358', metrics = CourseMetrics(homework_hours_per_week = "8", average_pass_rate = '40%'), professor = professor2, textbook = textbook2, course_location = location1)
    course2.save()

    professor1.course = course1
    professor1.textbook = textbook1
    professor1.location = location1
    professor1.save()

    professor2.course = course2
    professor2.textbook = textbook2
    professor2.location = location2
    professor2.save()

    location1.courses = [course1, course2]
    location1.textbook = textbook1
    location1.professor = professor1
    location1.save()

    location2.course = [course2]
    location2.textbook = textbook2
    location2.professor = professor2
    location2.save()

    textbook1.courses = [course1]
    textbook1.professor = professor1
    textbook1.location = location1
    textbook1.save()

    textbook2.courses = [course2]
    textbook2.professor = professor2
    textbook2.location = location2
    textbook2.save()