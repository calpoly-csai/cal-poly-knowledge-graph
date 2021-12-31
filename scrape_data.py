"""
Uses all active scrapers to fetch knowledge graph data from the web.
Run file with `python scrape_data.py`
"""

import importlib
import os
from scraper import registry
from mongoengine import connect
from argparse import ArgumentParser
from typing import List


connect("graphene-mongo-example", host="mongomock://localhost", alias="default")


def scrape_data(active_scrapers: List[str] = []):
    scrapers_filenames = [
        file.split(".")[0] for file in os.listdir("scrapers") if file.endswith(".py")
    ]
    for scraper_path in scrapers_filenames:
        importlib.import_module(f"scrapers.{scraper_path}")
    active_scrapers = (
        [scraper for scraper in registry if scraper.__name__ in active_scrapers]
        if len(active_scrapers) > 0
        else registry
    )
    for scraper_cls in active_scrapers:
        scraper = scraper_cls()
        scraper.scrape()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "scrapers",
        nargs="*",
        help="Space separated list of which scrapers to run. If omitted, all scrapers will run by default",
    )
    args = parser.parse_args()
    print(args.scrapers)
    scrape_data(args.scrapers)
