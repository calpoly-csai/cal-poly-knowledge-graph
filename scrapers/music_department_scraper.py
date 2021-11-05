from requests.models import codes
from models import Professor, Room
from autoscraper import AutoScraper
import os
from scraper import registry, Scraper
from bs4 import BeautifulSoup as bsp
import requests
from scrapers.departmentscraper import DepartmentScraper

# 1. Register your scraper so that it gets run by the scrape_data file. Make sure your class is a subclass of `Scraper`
@registry.register
class MusicDepartmentScraper(DepartmentScraper):
    """
    Fetches information about Cal Poly Music Department professors
    """

    # TODO: fix repetitive code
    # TODO: ReferenceField
    # TODO: Kramer sax shows up twice

    links = {"Music": "https://music.calpoly.edu/faculty/"}

    # 2. The only requirement of the class is the `scrape()` function. This will get data from the internet and upload it to the server.
    def scrape(self):
        name_bio_dict = (
            {}
        )  # used to deal with professors appearing multiple times, with different bios

        page = requests.get("https://music.calpoly.edu/faculty/")
        soup = bsp(page.content, "html.parser")

        """Faculty Table + Staff Table"""
        professor_data_html = soup.select("#mainLeftFull > table")
        four_column_tables = [0, 3]  # faculty and staff
        for table in four_column_tables:
            sub_soup = bsp(str(professor_data_html[table]), "html.parser")
            professor_data = sub_soup.find_all(
                "tr"
            )  # only looks at this specific table
            for prof in professor_data:
                attributes = prof.find_all(
                    "td"
                )  # list of attributes for a prof, has HTML Tags
                if len(attributes) > 0:
                    name = attributes[0].text.strip()
                    office = self.office_str_to_room(attributes[1].text.strip())
                    email = attributes[2].text.strip()
                    phone_number = attributes[3].text.strip()
                    bio = attributes[4].text.strip()  # "music area"
                    try:
                        prof = Professor.objects.get(name=name)
                        prof.office = office
                        prof.email = email
                        prof.phone_number = phone_number
                        prof.save()
                    except:
                        Professor(
                            name=name,
                            office=office,
                            email=email,
                            phone_number=phone_number,
                        ).save()
                    self.add_to_bio_dict(name_bio_dict, name, bio)

        """Faculty Lecturers"""
        professor_data_html = soup.select("#mainLeftFull > table:nth-child(5) > tbody")
        sub_soup = bsp(str(professor_data_html[0]), "html.parser")
        professor_data = sub_soup.find_all("tr")  # only looks at this specific table

        for prof in professor_data:
            attributes = prof.find_all(
                "td"
            )  # list of attributes for a prof, has HTML Tags
            if len(attributes) > 0:
                name = attributes[0].text.strip()
                office = self.office_str_to_room(attributes[1].text.strip())
                email = attributes[2].text.strip()
                bio = attributes[3].text.strip()  # "music area"
                try:
                    prof = Professor.objects.get(name=name)
                    prof.office = office
                    prof.email = email
                    prof.save()
                except:
                    Professor(name=name, office=office, email=email).save()
                self.add_to_bio_dict(name_bio_dict, name, bio)

        """Applied Faculty Table"""
        professor_data_html = soup.select(
            "#mainLeftFull > table:nth-child(8)"
        )  # .find_all("tr")
        sub_soup = bsp(str(professor_data_html[0]), "html.parser")
        professor_data = sub_soup.find_all("tr")  # only looks at this specific table

        for prof in professor_data:
            attributes = prof.find_all(
                "td"
            )  # list of attributes for a prof, has HTML Tags

            if len(attributes) > 0:
                name = attributes[0].text.strip()
                bio = attributes[1].text.strip()
                try:
                    prof = Professor.objects.get(name=name)
                    prof.save()
                except:
                    Professor(name=name).save()
                self.add_to_bio_dict(name_bio_dict, name, bio)
                x = set()

        for name, bio in name_bio_dict.items():
            bio_text = "Music Area: " + ", ".join(bio)
            try:
                prof = Professor.objects.get(name=name)
                prof.bio = bio_text
                prof.save()
            except:
                Professor(name=name, bio=bio_text).save()

    def add_to_bio_dict(self, name_bio_dict, name, bio):
        """creates a key-value pair between name and bio in name_bio_dict
        if key exists, appends bio to existing bio"""
        if name in name_bio_dict:
            bio_set = name_bio_dict[name]
            bio_set.update(bio.split(", "))
        else:
            bio_set = set()
            bio_set.update(bio.split(", "))
            name_bio_dict[name] = bio_set
