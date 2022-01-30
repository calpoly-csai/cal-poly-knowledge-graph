from models import (
    CovidInfo,
    CovidIsolationQuarantineStatus,
    DailyCovidTestRecord,
    DailyCovidCasesDetail,
    VaccinationStatus,
)
from bs4 import BeautifulSoup as bs
from scraper import registry, Scraper
import requests


# TODO: scraping dynamic website: https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f
# 1. Register your scraper so that it gets run by the scrape_data file. Make sure your class is a subclass of `Scraper`
@registry.register
class CovidScraper(Scraper):
    """
    Fetches information about Cal Poly colleges.
    """

    # 2. The only requirement of the class is the `scrape()` function. This will get data from the internet and upload it to the server.
    def scrape(self):
        page = requests.get("https://coronavirus.calpoly.edu/dashboard")
        soup = bs(page.content, "html.parser")

        # Get vaccination status - TODO: save it to parent doc
        content_boxes = soup.find_all("div", {"class": "contentBox"})
        vaccination_content_box = content_boxes[1]

        table_rows = vaccination_content_box.table.tbody.find_all("tr")[1:]
        for table_row in table_rows:
            group = table_row.th.get_text()
            population, num_vaccinated, percentage = [
                data.get_text().strip() for data in table_row.find_all("td")
            ]
            try:
                vaccination_status = VaccinationStatus.objects.get(group=group)
                vaccination_status.population = population
                vaccination_status.vaccinated = num_vaccinated
                vaccination_status.percentage_vaccinated = percentage
            except:
                vaccination_status = VaccinationStatus(
                    group=group,
                    population=population,
                    vaccinated=num_vaccinated,
                    percentage_vaccinated=percentage,
                )

        dashboard_iframe_page = requests.get("https://coviddashboard.calpoly.io/")
        ifram_soup = bs(dashboard_iframe_page.content, "html.parser")

        quarantine_isolation_box = ifram_soup.find_all("div", {"class": "row"})[4]

        quarantine_isolation_data = (
            quarantine_isolation_box.select_one(".col-sm-7")
            .select_one(".row.green")
            .find_all("div", {"class": "col"})
        )
        print(quarantine_isolation_data)
        for data in quarantine_isolation_data:
            print(data)
        # students_in_iso, students_in_quarantine, students_in_quarantine_in_place = [
        #     data.span.get_text() for data in quarantine_isolation_data
        # ]

        beds_data = (
            quarantine_isolation_box.select_one(".col-sm-5")
            .select_one(".row.green")
            .find_all("div", {"class": "col"})
        )
        beds_occupied, beds_available = [data.span.get_text() for data in beds_data]

        print(students_in_iso, students_in_quarantine, students_in_quarantine_in_place)
        print(beds_occupied, beds_available)

        # for college_name, url in self.links.items():
        #     try:
        #         college = College.objects.get(name=college_name)
        #     except:
        #         college = College(name=college_name)
        #     college.save()

        #     departments = scraper.get_result_similar(url)
        #     department_objects = []
        #     for department in departments:
        #         try:
        #             department_object = Department.objects.get(name=department)
        #         except:
        #             department_object = Department(name=department)
        #         department_object.college = college
        #         department_object.save()
        #         department_objects.append(department_object)
        #     college.departments = department_objects
        #     college.save()
