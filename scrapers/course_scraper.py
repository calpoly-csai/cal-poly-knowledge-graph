from models import Course, Department
from autoscraper import AutoScraper
import os
from scraper import registry, Scraper

# 1. Register your scraper so that it gets run by the scrape_data file. Make sure your class is a subclass of `Scraper`
@registry.register
class CourseScraper(Scraper):
    """
    Fetches information about Cal Poly courses.
    """

    # 2. The only requirement of the class is the `scrape()` function. This will get data from the internet and upload it to the server.
    def scrape(self):
        scraper = AutoScraper()
        base_url = "https://catalog.calpoly.edu/coursesaz/aero/"

        # Get links to all of the course pages.
        wanted = ["/coursesaz/agb/", "/coursesaz/agc/", "/coursesaz/aero/"]
        links = scraper.build(url=base_url, wanted_list=wanted)

        # Build a scraper that will scrape a course page, fetching the course name, description, and department
        scraper = AutoScraper()
        config_path = os.path.join("scrapers", "config", "course_scraper")
        if not os.path.exists(config_path):
            wanted = [
                "AERO 200. Special Problems for Undergraduates.",
                "Individual investigation, research, studies, or surveys of selected problems.  Total credit limited to 4 units.",
                "Aerospace Engineering (AERO)",
            ]
            res = scraper.build(url=base_url, wanted_list=wanted)
            scraper.save(config_path)
        scraper.load(config_path)

        # For every link, scrape for course data
        for link in links:
            url = "https://catalog.calpoly.edu" + link
            res = scraper.get_result_similar(url, grouped=True)
            data = list(res.values())

            names = data[0]
            descriptions = data[1]
            scraped_department = data[2][0].split(" (")[0]

            # Check if the department exists in the database, if not create a new department
            query_department = Department.objects(name=scraped_department)
            department = None
            if not query_department:
                department = Department(name=scraped_department).save()
            else:
                department = query_department[0]

            # Insert courses into the DB
            for i in range(min(len(names), len(descriptions))):
                course_id = names[i].split(".")[0]
                course_name = names[i].split(". ")[1]
                try:
                    course = Course.objects.get(course_id=course_id)
                    course.description = descriptions[i]
                    course.course_id = course_id
                    course.department = department
                    course.save()
                except:
                    Course(
                        name=course_name,
                        description=descriptions[i],
                        course_id=course_id,
                        department=department,
                    ).save()
