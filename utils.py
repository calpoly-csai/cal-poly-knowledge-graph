"""
Utility functions and variables used in multiple places throughout the codebase
"""

from enum import Enum

phone_number_regex = (
    r"(\d{3}[-\.\s]\d{3}[-\.\s]\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]\d{4}|\d{3}[-\.\s]\d{4})"
)
email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


class ProgramType(Enum):
    MAJOR = "major"
    MINOR = "minor"
    CONCENTRATION = "concentration"
    BS = "bs"
    MS = "ms"


class SectionType(Enum):
    LECTURE = "lecture"
    LAB = "lab"
    ACTIVITY = "activity"


class Weekday(Enum):
    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"


class Quarter(Enum):
    FALL = "Fall"
    WINTER = "Winter"
    SPRING = "Spring"
    SUMMER = "Summer"


class CourseType(Enum):
    """
    Course requirement type fulfilled by taking a class
    """

    # TODO: add more
    A1 = "A1"
    A2 = "A2"
