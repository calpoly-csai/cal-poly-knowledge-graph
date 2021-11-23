import os
from models import Professor
from bs4 import BeautifulSoup as bs
import requests
from scraper import registry
from scrapers.departmentscraper import DepartmentScraper

AREA_CODE_DASH = "805-"


@registry.register
class BioSciDepartmentScraper(DepartmentScraper):

    """
    Fetches information about Cal Poly's Biological Sciences Department.
    """

    links = {"Biology": "https://bio.calpoly.edu/content/faculty-and-staff"}

    def scrape(self):
        """Gets data from the internet and Uploads it to the server."""

        link = self.links["Biology"]

        page = requests.get(link)
        soup = bs(page.content, "html.parser")
        department = soup.find("div", class_="field-item even")
        tables = department.find_all("table")
        for num, table in enumerate(tables):
            people = table.find_all("tr")[1:]  # Exclude the headers
            for person in people:
                information = person.find_all("td")
                name = information[0].text.strip()

                """Default Values"""
                website = None
                email = None
                phone = None
                office = None
                office_hours = None

                pre_url = information[0].find("p")
                if pre_url is not None:
                    url = pre_url.find("a")["href"]
                    website = url
                if len(information[2].text.strip()) != 0:
                    """Empty tag"""
                    email = (
                        information[2].find("a")["href"].replace("mailto:", "").strip()
                    )
                if (
                    len(information[3].text.strip()) > 0
                    and information[3].text.strip() != "None"
                ):
                    """Cannot be empty nor None"""
                    phone = AREA_CODE_DASH + information[3].text.strip()
                if (
                    len(information[4].text.strip()) > 0
                    and information[4].text.strip() != "None"
                ):
                    pre_office = information[4].text.strip()
                    office = self.office_str_to_room(pre_office)
                if num < 5:
                    """Only Tables 0-4"""
                    office_hours = information[5].text.strip()

                """
                try:
                    prof = Professor.objects.get(name=name)
                    if email is not None:
                        prof.email = email
                    if phone is not None:
                        prof.phone_number = phone
                    if office is not None:
                        prof.office = office
                    if office_hours is not None:
                        prof.office_hours = office_hours
                    if website is not None:
                        prof.website = website
                    prof.save()
                except:
                    Professor(name=name, email=email, phone_number=phone,
                    office=office, office_hours=office_hours, website=website).save()
                """

    # Notes
    # Positions of the faculty members?
    # except block?
