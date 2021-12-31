from models import College, Department
from autoscraper import AutoScraper
import os
from scraper import registry, Scraper

# 1. Register your scraper so that it gets run by the scrape_data file. Make sure your class is a subclass of `Scraper`
@registry.register
class CollegeScraper(Scraper):
    """
    Fetches information about Cal Poly colleges.
    """

    links = {
        "Agriculture Food and Environmental Sciences": "https://www.calpoly.edu/college-of-agriculture-food-and-environmental-sciences",
        "Architecture and Environmental Design": "https://www.calpoly.edu/college-of-architecture-and-environmental-design",
        "Engineering": "https://www.calpoly.edu/college-of-engineering",
        "Liberal Arts": "https://www.calpoly.edu/college-of-liberal-arts",
        "Science and Mathematics": "https://www.calpoly.edu/college-of-science-and-mathematics",
        "Business": "https://www.calpoly.edu/orfalea-college-of-business",
    }

    # 2. The only requirement of the class is the `scrape()` function. This will get data from the internet and upload it to the server.
    def scrape(self):
        scraper = AutoScraper()
        config_path = os.path.join("scrapers", "config", "college_scraper")
        if not os.path.exists(config_path):
            url = self.links[0]
            wanted = ["Agricultural Business"]
            res = scraper.build(url=url, wanted_list=wanted)
            scraper.save(config_path)
        scraper.load(config_path)
        for college_name, url in self.links.items():
            try:
                college = College.objects.get(name=college_name)
            except:
                college = College(name=college_name)
            college.save()

            departments = scraper.get_result_similar(url)
            department_objects = []
            for department in departments:
                try:
                    department_object = Department.objects.get(name=department)
                except:
                    department_object = Department(name=department)
                department_object.college = college
                department_object.save()
                department_objects.append(department_object)
            college.departments = department_objects
            college.save()
