from models import College, Department
from bs4 import BeautifulSoup as bs
import os
import requests
from scraper import registry, Scraper
from typing import Dict, List, TypedDict

# 1. Register your scraper so that it gets run by the scrape_data file. Make sure your class is a subclass of `Scraper`
@registry.register
class CollegeScraper(Scraper):
    """
    Fetches information about Cal Poly colleges.
    """

    def parse_colleges(self, soup):
        colleges = []
        contents = soup.find("div", id="textcontainer")
        college = None
        for div_child in contents:
            if div_child == "\n":
                continue
            if div_child.name == "p":
                link = div_child.find("a")
                college_name = str(link.text)
                college_web_url = "https://catalog.calpoly.edu" + link["href"]
                college = {"name": college_name, "url": college_web_url}

            if div_child.name == "ul":
                college["departments"] = []
                department_links = div_child.find_all("a")
                for link in department_links:
                    url = "https://catalog.calpoly.edu" + link["href"]
                    name = str(link.text)
                    college["departments"].append({"name": name, "url": url})
                colleges.append(college)
                college = None
        return colleges

    class ProgramInfo(TypedDict):
        name: str
        degrees: List[str]

    def parse_college_programs(self, college_url: str) -> List[ProgramInfo]:
        programs = []
        res = requests.get(college_url)
        page = bs(res.content, "html.parser")

        table = page.find("tbody")
        for row in table.find_all("tr"):
            cols = row.find_all("td")
            name = cols[0].text
            degrees = cols[1].text.split(",")
            # degrees = degrees.split(",")
            programs.append({"name": name, "degrees": degrees})
        return programs

    def parse_department_programs(self, department_url: str) -> List[Dict[str, str]]:
        programs = []
        res = requests.get(department_url)
        page = bs(res.content, "html.parser")
        table = page.find("tbody")

        for row in table.find_all("tr"):
            cols = row.find_all("td")
            name = cols[0].text
            degrees = cols[1].text
            degrees = degrees.split(",")
            programs.append({"name": name, "degrees": degrees})
        return programs

    # 2. The only requirement of the class is the `scrape()` function. This will get data from the internet and upload it to the server.
    def scrape(self):
        colleges = []
        url = "https://catalog.calpoly.edu/collegesanddepartments/"
        res = requests.get(url)
        soup = bs(res.content, "html.parser")

        # BS, BA, MS, MA, Minor, Master of
        colleges = self.parse_colleges(soup)
        for college in colleges:
            self.parse_college_programs(college["url"])
            for dep in college["departments"]:
                self.parse_department_programs(dep["url"])

        # TODO:
        # - Update programs in database
        # - Connect programs to college or department (we could do these updates in funcs ^)
        # - college_programs U department_programs

        for college_data in colleges:
            try:
                college = College.objects.get(name=college_data["name"])
            except:
                college = College(name=college_data["name"])
            college.save()

            department_objects = []
            for department_data in college_data["departments"]:
                try:
                    department_object = Department.objects.get(
                        name=department_data["name"]
                    )
                except:
                    department_object = Department(name=department_data["name"])
                department_object.college = college
                department_object.save()
                department_objects.append(department_object)
            college.departments = department_objects
            college.save()
