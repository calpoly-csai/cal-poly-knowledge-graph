import os
from models import Professor
from bs4 import BeautifulSoup as bs
import requests
from scraper import registry
from scrapers.departmentscraper import DepartmentScraper


@registry.register
class ChemDepartmentScraper(DepartmentScraper):

    """
    Fetches information about Cal Poly's Chemistry/Biochemistry Department.
    """

    links = {
        "Chemistry and Biochemistry": "https://chemistry.calpoly.edu/content/about-us/Chemistry%26BiochemistryDirectory"
    }

    def scrape(self):
        """Gets data from the internet and Uploads it to the server."""

        link = self.links["Chemistry and Biochemistry"]

        page = requests.get(link)
        soup = bs(page.content, "html.parser")
        directory = soup.find("table", class_="directory")  # DEPARTMENT
        tables = directory.find_all("table", class_="directory")  # DEPARTMENT SECTIONS

        for num, table in enumerate(tables):
            people = table.find_all("tr")[1:]  # EXCLUDE THE HEADERS

            if num == 2:
                # CURRENT FULL-TIME FACULTY
                for person in people:

                    attributes = {}  # Attributes of the Faculty Member

                    information = person.find_all("td")

                    # NAME
                    if information[0].find("p") is not None:
                        # If Professor's name is surrounded in p tags
                        attributes["name"] = information[0].find("p").text
                    else:
                        attributes["name"] = information[0].text

                    # POSITION
                    bio = f"Position: {information[1].text}"
                    attributes["bio"] = bio

                    # EMAIL
                    if information[2].find("p") is not None:
                        # If Professor's email is surrounded in p tags
                        attributes["email"] = information[2].find("p").text
                    else:
                        attributes["email"] = information[2].text

                    # WEBSITE
                    url = (person.find("a"))["href"]
                    if "https://chemistry.calpoly.edu" not in url:
                        url = f"https://chemistry.calpoly.edu{url}"

                    attributes["website"] = url

                    try:
                        prof = Professor.objects.get(name=attributes["name"])
                        prof.bio = attributes["bio"]
                        prof.email = attributes["email"]
                        prof.website = attributes["website"]
                        prof.save()
                    except:
                        prof = Professor(name=attributes["name"])
                        for attribute in attributes.keys():
                            if attribute == "bio":
                                prof.bio = attributes["bio"]
                            if attribute == "email":
                                prof.email = attributes["email"]
                            if attribute == "website":
                                prof.website = attributes["website"]
                        prof.save()

            if num < 2 or num == 3:
                # DEPARTMENT OFFICE, TECHNICAL STAFF, FACULTY EMERITI
                for person in people:

                    attributes = {}  # Attributes of the Faculty Member

                    information = person.find_all("td")

                    # NAME
                    name = information[0].text
                    attributes["name"] = name

                    # EMAIL
                    email = information[1].text.strip()
                    if len(email) > 0:
                        attributes["email"] = email

                    # WEBSITE
                    url = (person.find("a"))["href"]
                    if "https://chemistry.calpoly.edu" not in url:
                        url = f"https://chemistry.calpoly.edu{url}"
                    attributes["website"] = url

                    try:
                        prof = Professor.objects.get(name=attributes["name"])
                        if len(email) > 0:
                            # If they do not have an email
                            prof.email = attributes["email"]
                        prof.website = attributes["website"]
                        prof.save()
                    except:
                        prof = Professor(name=attributes["name"])
                        for attribute in attributes.keys():
                            if attribute == "email":
                                prof.email = attributes["email"]
                            if attribute == "website":
                                prof.website = attributes["website"]
                        prof.save()
