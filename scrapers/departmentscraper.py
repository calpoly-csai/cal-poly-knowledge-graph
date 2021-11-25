"""
subclass of scraper that provides some helpful functions for scraping for professor
"""

from scraper import Scraper
from models import Room, OfficeHours
import unicodedata


class DepartmentScraper(Scraper):
    def office_str_to_room(self, office):
        """converts office strings (e.g. '45-121') into room objects"""
        # TODO: building number to building name utils?
        # CURRENTLY BUILDING NAME IS JUST ITS NUMBER
        split_string = office.split("-")
        if len(split_string) == 2:
            building_number = split_string[0]
            room_number = split_string[1]
        elif len(split_string) == 1 and split_string[0] != "":
            building_number = office  # to handle the office = "45M" case
            room_number = office
        else:
            return None
        try:
            room = Room.objects.get(
                building_name=building_number, room_number=room_number
            )
            return room
        except:
            room = Room(building_name=building_number, room_number=room_number)
            room.save()
            return room

    def check_days(self, p_text):
        """Helper Function for bio_office_hours_str_to_object"""
        """Checks if the p_tag contains a day, otherwise it is just a zoom link"""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for day in days:
            if day in p_text:
                if "appt" not in p_text:
                    # Appointment days do not have start or end times
                    return True
        return False

    def bio_office_hours_str_to_object(self, office_hours):
        """Converts office hours strings into office hours objects for BIO Department"""
        """Is it possible to generalize this?"""
        oh_text = office_hours.text.strip()

        # Professors who DO NOT have office hours have blank boxes or write None

        if len((oh_text)) > 0:  # No blank boxes
            if oh_text.lower() != "none":  # None is not written in office hours section

                oh_all = []  # All Office Hours of the Person

                link = None
                # OFFICE HOURS LINK
                if (office_hours.find("a")) is not None:
                    # They have an office hour link!
                    link = (office_hours.find("a"))["href"]

                # DAYS AND TIMES
                p_tags = office_hours.find_all("p")
                for p_tag in p_tags:
                    text = p_tag.text
                    if self.check_days(
                        text
                    ):  # Filters p_tags that do not contain weekdays
                        normalized = unicodedata.normalize("NFKD", p_tag.text)
                        dates = normalized.split("-", 1)

                        # DAYS
                        days = [dates[0].strip()]  # list of days

                        if (
                            len(days[0]) > 9
                        ):  # there is more than 1 day (Wednesday has the most letters)
                            mult_days = dates[0].replace(",", "&").split("&")
                            mult_days = [item.strip() for item in mult_days]
                            days = mult_days

                        # TIMES (Only taking the first time period of office hours)
                        # For example, if there are two office hours on the same day, take the first one
                        times = dates[1].strip()

                        # FIX NOON TO BE 12:00
                        if "Noon" in times:
                            times = times.replace("Noon", "12:00")

                        if len(times) > 0:
                            # There is some text
                            if times[0].isdigit():
                                # If the first character is a digit, there is a time period
                                splitted_1 = times.split("-", 1)  # split for the dash
                                splitted_2 = (splitted_1[1].strip()).split(
                                    " ", 1
                                )  # take the 2nd half and grab the end time
                                start_time = splitted_1[0]
                                end_time = splitted_2[0]
                                if (
                                    "pm" in end_time
                                ):  # The case when there was a pm in the end time
                                    end_time = end_time.replace("pm", "")

                                # Create new Office Hours object
                                oh = OfficeHours(
                                    start_time=start_time, end_time=end_time
                                )
                                if link != None:
                                    oh.link = link
                                oh.weekdays = days
                                oh_all.append(oh)
                return oh_all
        return None
