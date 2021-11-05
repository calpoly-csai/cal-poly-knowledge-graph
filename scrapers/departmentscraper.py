"""
subclass of scraper that provides some helpful functions for scraping for professor
"""

from scraper import Scraper
from models import Room


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
