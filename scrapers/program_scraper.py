from models import Program, Department
from autoscraper import AutoScraper
import os
from scraper import registry, Scraper
from bs4 import BeautifulSoup as bsp
from urllib.request import Request, urlopen

# 1. Register your scraper so that it gets run by the scrape_data file. Make sure your class is a subclass of `Scraper`
@registry.register
class ProgramScraper(Scraper):
    """
    Fetches information about Cal Poly programs.
    """

    # 2. The only requirement of the class is the `scrape()` function. This will get data from the internet and upload it to the server.
    def scrape(self):
        base_url = "https://catalog.calpoly.edu/collegesanddepartments/"

        links: list[str] = []
        departments: list[str] = []

        soup = bsp(
            urlopen(Request(base_url, headers={"User-Agent": "Mozilla/5.0"})),
            "html.parser",
        )
        container = soup.find_all("div", {"id": "textcontainer"})
        unordered_lists = container[0].find_all("ul")

        for ul in unordered_lists:
            list_items = ul.find_all("li")
            for li in list_items:
                link = li.find("a", href=True)
                departments.append(link.text)
                links.append("https://catalog.calpoly.edu" + link["href"])

        # For every link, scrape for program data
        for link_index, link in enumerate(links):
            soup = bsp(
                urlopen(Request(link, headers={"User-Agent": "Mozilla/5.0"})),
                "html.parser",
            )
            program_names = soup.find_all("td", {"class": "column0"})
            program_types = soup.find_all("td", {"class": "column1"})

            # Check if the department exists in the database, if not create a new department
            query_department = Department.objects(name=departments[link_index])
            department = None
            if not query_department:
                department = Department(name=departments[link_index]).save()
            else:
                department = query_department[0]

            for index, program_name in enumerate(program_names):
                program_type = program_types[index].text.split(", ")
                try:
                    program = Program.objects.get(name=program_name.text)
                    program.department = department
                    program.program_types = program_type
                    program.save()
                except:
                    Program(
                        name=program_name.text,
                        department=department,
                        program_types=program_type,
                    ).save()
