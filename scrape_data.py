"""
Uses all active scrapers to fetch knowledge graph data from the web.
Run file with `python scrape_data.py`
"""

import importlib
import os
from scraper import registry
from mongoengine import connect


connect('graphene-mongo-example', host='mongomock://localhost', alias='default')
    





def main():
    scrapers_filenames = [file.split(".")[0] for file in os.listdir("scrapers") if file.endswith(".py")]

    for scraper_path in scrapers_filenames:
        importlib.import_module(f"scrapers.{scraper_path}")
        
    for scraper_cls in registry:
        scraper = scraper_cls()
        scraper.scrape()

if __name__ == "__main__":
    main()