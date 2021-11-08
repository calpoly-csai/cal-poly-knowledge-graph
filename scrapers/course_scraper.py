from models import Course, Department
from requests.models import codes
from scraper import registry, Scraper
from bs4 import BeautifulSoup as bsp
from urllib.request import Request, urlopen

@registry.register
class CourseScraper(Scraper):
    """
    Fetches information about Cal Poly courses
    """

    # TODO add option to pass in single Department to get its courses 
    # TODO only required fields have been done

    def scrape(self):
        course_link_dictionary = self.getAllCourseLinks()
        # Each key is a department name OR College name if there is no corresponding department
        course_keys = course_link_dictionary.keys()
        for key in course_keys:
            # TODO get Department object from somewhere else to avoid duplicates
            course_department = Department(name = key).save()
            links = course_link_dictionary[key]
            for link in links:
                soup = bsp(urlopen(Request("https://catalog.calpoly.edu" + link, headers={"User-Agent": "Mozilla/5.0"})), "html.parser")
                courseblocks = soup.find_all("div", {"class" : "courseblock"})
                for courseblock in courseblocks:
                    
                    ID_name = courseblock.find("strong").text
                    split_str = ID_name.split(".")
                    course_ID = split_str[0]
                    course_name = split_str[1].strip()
                    # TODO some courses also aren't a fixed amount -> e.g. AG200 is 1-2 units
                    # TODO some units are also aren't integers. e.g. ESM90 is 1.5 units
                    course_units = int(float(courseblock.find("span", {"class" : "courseblockhours"}).text[:-6].strip().split("-")[0]))
                    course_description = courseblock.find("div", {"class" : "courseblockdesc"}).p.text
                
                    course = Course(name = course_name,
                        description = course_description,
                        course_id = course_ID,
                        units = course_units,
                        department = course_department).save()



    # gets links to all course pages
    def getAllCourseLinks(self):
        site = "https://catalog.calpoly.edu/coursesaz/"
        soup = bsp(urlopen(Request(site, headers={"User-Agent": "Mozilla/5.0"})), "html.parser")
        section = soup.find("div", {"id" : "courseprefixestextcontainer"})

        course_links = {}
        # Some courses belong to an entire college and don't have specific departments (e.g. ENGR, SCM, etc)
        # Notably, Orfalea doesn't have departments at all
        # This loop also includes Extended Education
        for p in section.find_all('p'): 
            current_dept_name = ""
            for child in p.children:
                if (child.name == "strong"):
                    current_dept_name = child.string.strip()
                    course_links[current_dept_name] = []
                elif (child.name == 'a'):
                    course_links[current_dept_name].append(child['href'])
            if not course_links[current_dept_name]:
                course_links.pop(current_dept_name)

        # Links for all departments are handled in this loop
        for ul in section.find_all("ul"):
            for li in ul.find_all("li"):
                dept_name = str(li).split("(")[0][4:].strip()
                course_list = []
                for a in li.find_all('a', href=True):
                    course_list.append(a['href'])
                course_links[dept_name] = course_list

        return course_links