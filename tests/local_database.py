# flask_graphene_mongo/database.py
from mongoengine import connect

from models import *

connect("graphene-mongo-example", host="mongomock://localhost", alias="default")


def init_db():
    """
    Creates test data in an local database for development purposes.
    """
    # Colleges
    engineering = College(
        name="Engineering",
        description="A national leader in engineering education, the College of Engineering promotes project-based learning to link theory with hands-on practice to solve the future’s most pressing technical challenges.",
    )
    business = College(
        name="College of Business",
        description="At the Orfalea College of Business, you gain expertise in the fields of management, finance, economics and entrepreneurship by working with real companies in your community and developing your own business ideas.",
    )
    agriculture = College(
        name="Agriculture, Food, and Environmental Sciences",
        description="One of the nation’s most prestigious undergraduate agriculture programs, the College of Agriculture, Food and Environmental Sciences takes you into the field, the farm and the forest to apply cutting-edge techniques to the ancient challenge of feeding a growing society.",
    )
    architecture = College(
        name="Architecture and Environmental Design",
        description="The College of Architecture and Environmental Design offers a hands-on approach to working in all aspects of the built environment, from designing homes and gardens to planning cities.",
    )
    liberal_arts = College(
        name="Liberal Arts",
        description="The College of Liberal Arts houses fifteen departments offering programs in the humanities, social sciences, communications and performing arts that share focus on the evolving nature of human experience and expression in the modern world.",
    )
    science_math = College(
        name="Science and Mathematics",
        description="The College of Science and Mathematics prepares you to become a leader in an increasingly scientific and technological society through education, research and practical experience.",
    )

    engineering.save()
    business.save()
    agriculture.save()
    architecture.save()
    liberal_arts.save()
    science_math.save()

    # Departments (only engineering for now)
    eng_departments = [
        Department(name=name, college=engineering)
        for name in [
            "Aerospace Engineering",
            "Architectural Engineering",
            "Biomedical Engineering",
            "BioResource and Agricultural Engineering",
            "Civil Engineering",
            "Computer Engineering",
            "Electrical Engineering",
            "Environmental Engineering",
            "General Engineering",
            "Industrial Engineering",
            "Liberal Arts and Engineering Studies",
            "Manufacturing Engineering",
            "Materials Engineering",
            "Mechanical Engineering",
            "Software Engineering",
        ]
    ]

    cs_dep = Department(
        name="Computer Science & Software Engineering",
        description=" degree in computer science prepares you to design and develop computer technologies such as operating systems, websites and mobile apps, artificial intelligence suites, software for robotics, search engines and more.Modern labs help you gain a practical understanding of computer science – from learning algorithmic problem solving to the high-level programming languages. Individual and team projects, as well as internships and co-ops throughout California's technology hubs, reinforce the concepts learned and provide you the opportunity to apply and communicate your knowledge. The program is accredited by the Engineering Accreditation Commission of ABET.",
    )
    eng_departments.append(cs_dep)

    for dep in eng_departments:
        dep.save()

    engineering.departments = eng_departments
    engineering.save()

    # Programs (only cs for now)

    cs_desc = """
    US News & World Report and other national publications recognize Cal Poly as having one of the best undergraduate computer science programs in the country. What makes the program stand out are: its very talented students, strong interactions with faculty on industry projects, a deep commitment to teaching, and laboratories with up-to-date technology.

The Computer Science program is accredited by the Computing Accreditation Commission of ABET.

http://www.abet.org

Class sizes are kept small — rarely more than 35 students — and are taught by the Computer Science faculty, not graduate students. Most courses in the major have a strong laboratory component.

Educational Objectives

The computer science program has four broad program educational objectives (PEOs) that graduates are expected to attain within five years of graduation:

Technical Competence. Graduates have applied current technical knowledge and skills to develop effective computer solutions, using state-of-the art technologies.
Interpersonal Skills. Graduates have communicated effectively and worked collaboratively in a team environment.
Professional Awareness. Graduates have maintained a positive and ethical attitude concerning the computing profession and its impact on individuals, organizations and society.
Intellectual Growth. Graduates have continued to grow intellectually and professionally in their chosen field, including successful pursuit of graduate study if such study was a desired goal.
Student Learning Outcomes

Graduates of the program will have an ability to:

Analyze a complex computing problem and to apply principles of computing and other relevant disciplines to identify solutions.
Design, implement, and evaluate a computing-based solution to meet a given set of computing requirements in the context of the program’s discipline.
Communicate effectively in a variety of professional contexts.
Recognize professional responsibilities and make informed judgments in computing practice based on legal and ethical principles.
Function effectively as a member or leader of a team engaged in activities appropriate to the program’s discipline.
Apply computer science theory and software development fundamentals to produce computing-based solutions.
    """

    data_sci_desc = """
    Through an inter-college collaboration, the Computer Science and Statistics departments offer a cross-disciplinary minor in Data Science — a rapidly evolving discipline that uses elements of statistics and computer science to gather, organize, summarize, and communicate information from a variety of data sources and data types.   Job opportunities for data scientists are growing as the availability of data becomes ever abundant via the internet, consumer transactions, sensor arrays, medical records, embedded biometrics, bionformatics, etc.

The CDSM provides an opportunity for both statistics and computer science students to complement their major training with foundational skills for data science.  Statistics majors will acquire essential programming, database, distributed computing, and data mining skills from the Computer Science Department while computer science majors will acquire essential probability, regression modeling, statistical programming, and multivariate analysis skills from the Statistics Department.


    """
    cs_progs = []
    cs = Program(name="B.S. Computer Science", description=cs_desc)
    cs_progs.append(cs)
    cs_progs.append(Program(name="M.S. Computer Science", graduate_level=True))
    cs_progs.append(Program(name="B.S. Software Engineering"))
    cs_progs.append(Program(name="B.S. Software Engineering"))
    cs_progs.append(Program(name="Computer Science Minor", program_types=["minor"]))
    cs_progs.append(
        Program(name="Computing for Interactive Arts Minor", program_types=["minor"])
    )
    cs_progs.append(
        Program(
            name="Cross Disciplinary Studies Minor in Bioinformatics",
            program_types=["minor"],
        )
    )
    cs_progs.append(
        Program(
            name="Cross Disciplinary Studies Minor in Data Science",
            description=data_sci_desc,
            program_types=["minor"],
        )
    )

    for prog in cs_progs:
        prog.department = cs_dep
        prog.save()
    cs_dep.programs = cs_progs
    cs_dep.save()

    # Courses
    csc_courses = []
    csc_courses.append(
        Course(
            name="Fundamentals of Computer Science",
            course_id="CSC 101",
            description="Basic principles of algorithmic problem solving and programming using methods of top-down design, stepwise refinement and procedural abstraction. Basic control structures, data types, and input/output. Introduction to the software development process: design, implementation, testing and documentation. The syntax and semantics of a modern programming language.",
            units=4,
            usually_offered=["Fall", "Winter", "Spring"],
        )
    )
    csc_courses.append(
        Course(
            name="Data Structures",
            description="Introduction to data structures and analysis of algorithms. Abstract datatypes. Specification and implementation of advanced data structures. Theoretical and empirical analysis of recursive and iterative algorithms. Software performance evaluation and testing techniques.",
            course_id="CSC 202",
            units=4,
            usually_offered=["Winter"],
        )
    )
    csc_courses.append(
        Course(
            name="Project-Based Object-Oriented Programming and Design",
            description="Object-oriented programming and design with applications to project construction. Introduction to class design, interfaces, inheritance, generics, exceptions, streams, and testing.",
            course_id="CSC 203",
            units=4,
            usually_offered=["Winter"],
        )
    )

    for course in csc_courses:
        course.department = cs_dep
    for i in range(1, len(csc_courses)):
        csc_courses[i].prerequisites = [csc_courses[i - 1]]
    for course in csc_courses:
        course.save()

    cs.curriculum = csc_courses
    cs.save()
