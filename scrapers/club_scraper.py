import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Club
import requests
import json
import time


"""
Cal poly now api: https://calpoly.campuslabs.com/engage/api/discovery/
Link to clubs: https://calpoly.campuslabs.com/engage/api/discovery/search/organizations


https://calpoly.campuslabs.com/engage/api/discovery/search/organizations?orderBy%5B0%5D=UpperName%20asc&top=1000&filter=&query=&skip=0

Officer information here: "https://calpoly.campuslabs.com/engage/api/discovery/organization/324945/position?take=100&isOfficer=true"

"""


def main():
    full_club_list_link = "https://calpoly.campuslabs.com/engage/api/discovery/search/organizations/?top=10000"
    club_link = "https://calpoly.campuslabs.com/engage/api/discovery/organization/"
    # ex: 'https://calpoly.campuslabs.com/engage/api/discovery/organization/324945'

    club_list = requests.get(full_club_list_link).json()["value"]
    club_codes = []  # list of club ids to reach each club's webpage
    for club in club_list:
        club_codes.append(club["Id"])
    # with open("club_dicts.txt", 'w') as file:
    for code in club_codes:
        specific_club_link = club_link + code
        officer_link = f"https://calpoly.campuslabs.com/engage/api/discovery/organization/{code}/position?take=100&isOfficer=true"
        club_dict = requests.get(specific_club_link).json()
        officer_dict = requests.get(officer_link)
        print(json.dumps(officer_dict.json(), indent=4))
        return
        # file.write(json.dumps(club_dict,indent=4))
        # file.write("\n\n")
        try:

            """ Club info """
            name = club_dict["name"]
            officers = []  # might have to be logged in to see officer names
            email = club_dict["email"]
            phone = club_dict["contactInfo"][0]["phoneNumber"]
            social_media = club_dict["socialMedia"]
            advisor = (
                None
            )  # no direct advisor info on cal poly now, might be part of the officers under a title of advisor

            """ Officers """
            # name = StringField(required=True)
            # major = StringField()
            # position = StringField()
            # email = StringField(regex=email_regex)

            # Clubs
            # name = StringField(required=True)
            # officers = EmbeddedDocumentListField(Officer, required=True)
            # email = StringField(regex=email_regex)
            # phone = StringField(regex=phone_number_regex)
            # social_media: DictField()
            # advisor = StringField()

            # # Officers
            # name = StringField(required=True)
            # major = StringField()
            # position = StringField()
            # email = StringField(regex=email_regex)

        except KeyError as e:
            print(e)


if __name__ == "__main__":
    print(
        json.dumps(
            requests.get(
                "https://now.calpoly.edu/api/discovery/organization/324844/member"
            ),
            indent=4,
        )
    )
    main()
