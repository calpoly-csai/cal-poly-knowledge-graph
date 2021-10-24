from requests.models import codes
from models import Professor, Room
from autoscraper import AutoScraper
import os
from scraper import registry, Scraper
from scrapers.departmentscraper import DepartmentScraper
from bs4 import BeautifulSoup as bsp
import requests
from urllib.request import Request, urlopen  # TODO: temp
import re

# 1. Register your scraper so that it gets run by the scrape_data file. Make sure your class is a subclass of `Scraper`
@registry.register
class CSCDepartmentScraper(DepartmentScraper):
    """
    Fetches information about Cal Poly Music Department professors
    """

    links = {
        "Computer Science and Software Engineering": "https://csc.calpoly.edu/faculty/"
    }

    # 2. The only requirement of the class is the `scrape()` function. This will get data from the internet and upload it to the server.
    def scrape(self):
        site = "https://csc.calpoly.edu/faculty/"
        hdr = {"User-Agent": "Mozilla/5.0"}
        req = Request(site, headers=hdr)
        page = urlopen(req)

        soup = bsp(page, "html.parser")

        """Faculty Table + Affiliated Faculty + Active Emeriti"""
        tables = soup.find_all("tbody")  # currently returns 4 tables
        for i in range(0, 3):
            professor_list = tables[i].find_all("tr")
            for prof in professor_list:
                attributes = prof.find_all("td")
                name_and_position = attributes[0].text
                website = attributes[0].find("a")
                if website is not None:
                    website = website.get("href")
                split_name_pos = re.split(
                    "\xa0–\xa0|\xa0– | –\xa0| – ", name_and_position
                )  # en dash, not regular dash
                name, position = split_name_pos[0], ", ".join(split_name_pos[1:])
                bio = "Position: " + position
                email = attributes[1].text
                office = self.office_str_to_room(attributes[2].text)
                try:
                    prof = Professor.objects.get(name=name)
                    prof.email = email
                    prof.office = office
                    prof.website = website
                    prof.bio = bio
                except:
                    Professor(
                        name=name, email=email, office=office, website=website, bio=bio
                    ).save()

        """Staff"""
        professor_list = tables[3].find_all("tr")  # staff is the 4th table
        is_header_table = (
            True
        )  # this last table doesn't have its key in <thead>, it's instead in the first row of <tbody>
        for prof in professor_list:

            if is_header_table:
                is_header_table = False
                continue

            attributes = prof.find_all("td")
            name = attributes[0].text
            website = attributes[0].find("a")
            if website is not None:
                website = website.get("href")
            position = attributes[1].text
            email = attributes[2].text
            bio = "Position: " + position

            try:
                prof = Professor.objects.get(name=name)
                prof.email = email
                prof.bio = bio
                prof.website = website
            except:
                Professor(
                    name=name, email=email, office=office, website=website, bio=bio
                ).save()
