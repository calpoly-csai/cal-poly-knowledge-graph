import os
from models import Professor, OfficeHours
from bs4 import BeautifulSoup as bs
import requests
from scraper import registry
from scrapers.departmentscraper import DepartmentScraper


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

                attributes = {}  # Attributes of Members
                information = person.find_all("td")

                # NAME
                name = " ".join(
                    (information[0].text.strip()).split(",")[::-1]
                )  # First-Last Name
                attributes["name"] = name

                # POSITION
                position = information[1].text.strip()
                if information[1].find("p") is not None:
                    name_parts = [p.text.strip() for p in information[1].find_all("p")]
                    position = " ".join(name_parts)
                attributes["bio"] = f"Position: {position}"

                # WEBSITE
                url = information[0].find("a")
                if url is not None:
                    url = url["href"]
                    if "https://bio.calpoly.edu" not in url:
                        if "https://cab.calpoly.edu" not in url:
                            url = f"https://bio.calpoly.edu{url}"
                    attributes["website"] = url

                # EMAIL
                if len(information[2].text.strip()) != 0:
                    """They have an email"""
                    email = (
                        information[2].find("a")["href"].replace("mailto:", "").strip()
                    )
                    if "@calpoly.edu" not in email:
                        email = f"{email}@calpoly.edu"
                    attributes["email"] = email

                # PHONE
                if (
                    len(information[3].text.strip()) > 0
                    and information[3].text.strip() != "None"
                ):
                    # Cannot be empty nor None
                    phone = information[3].find("a")
                    if phone is not None:
                        # The phone number has a link
                        phone = (phone["href"]).replace("tel:", "")
                        attributes["phone"] = phone
                    else:
                        # The phone number DOES NOT have a link
                        phone = f"805-{information[3].text.strip()}"
                        attributes["phone"] = phone

                # OFFICE
                if len(information[4].text.strip()) > 0:
                    pre_office = information[4].text.strip()
                    office = self.office_str_to_room(pre_office)
                    attributes["office"] = office

                # OFFICE HOURS
                if num < 5:
                    # Only Tables 0-4 have office hours
                    office_hours = information[5]
                    ohs = None
                    if num == 0:  # Department Chair and Administration
                        # OFFICE HOURS LINK
                        oh_all = []  # All Office Hours of Member
                        link = None
                        if (office_hours.find("a")) is not None:
                            # They have an office hour link!
                            link = (office_hours.find("a"))["href"]

                        p_tags = office_hours.find_all("p")
                        for p_tag in p_tags:
                            if len(p_tag.text.strip()) > 0:
                                if (p_tag.find("a")) is None:
                                    # FIX NOON TO BE 12:00
                                    p_text = p_tag.text
                                    if "Noon" in p_text:
                                        p_text = p_text.replace("Noon", "12:00")
                                    splitted_1 = p_text.split(":", 1)  # Day : Times
                                    splitted_2 = splitted_1[1].split(
                                        "-", 1
                                    )  # Start Time - End Time
                                    day = [splitted_1[0].strip()]
                                    start = splitted_2[0].strip()
                                    end = splitted_2[1].strip()

                                    oh = OfficeHours(start_time=start, end_time=end)
                                    if link != None:
                                        oh.link = link
                                    oh.weekdays = day
                                    oh_all.append(oh)
                        if len(oh_all) > 0:
                            attributes["office_hours"] = oh_all

                    else:  # Faculty and Lecturers
                        ohs = self.bio_office_hours_str_to_object(office_hours)
                    if ohs is not None:
                        # They have office hours
                        attributes["office_hours"] = ohs

                try:
                    # Retrieve the Professor
                    prof = Professor.objects.get(name=attributes["name"])
                    prof.bio = attributes["bio"]
                    for attribute in attributes.keys():
                        if attribute == "email":
                            prof.email = attributes["email"]
                        if attribute == "phone":
                            prof.phone_number = attributes["phone"]
                        if attribute == "office":
                            prof.office = attributes["office"]
                        if attribute == "office_hours":
                            prof.office_hours = attributes["office_hours"]
                        if attribute == "website":
                            prof.website = attributes["website"]
                    prof.save()
                except:
                    # If Professor isn't already saved, create a new Professor object and save it
                    prof = Professor(name=attributes["name"])
                    prof.bio = attributes["bio"]
                    for attribute in attributes.keys():
                        if attribute == "email":
                            prof.email = attributes["email"]
                        if attribute == "phone":
                            prof.phone_number = attributes["phone"]
                        if attribute == "office":
                            prof.office = attributes["office"]
                        if attribute == "office_hours":
                            prof.office_hours = attributes["office_hours"]
                        if attribute == "website":
                            prof.website = attributes["website"]
                    prof.save()
