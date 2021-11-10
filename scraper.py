"""
Contains the top-level logic that is used for creating and synchronizing web scrapers.
Create new web scrapers in the `scrapers` directory.
"""

from abc import ABC, abstractmethod

from typing import Dict


class Scraper(ABC):
    @abstractmethod
    def scrape(self):
        """
        Get data from the web and updates the knowledge graph server.
        """
        pass


class _ScraperRegistry:
    """
    Singleton class that collects references to all of the scrapers so that they can be easily run.
    """

    _scrapers: Dict[str, Scraper] = dict()

    def __len__(self):
        return len(self._scrapers)

    def __getitem__(self, index) -> Scraper:
        return list(self._scrapers.values())[index]

    @classmethod
    def register(cls, scraper):
        """
        Adds scraper to the scraper registry
        """
        assert issubclass(
            scraper, Scraper
        ), "All scrapers must inherit from habitat_sim.utils.data.PoseExtractor"

        cls._scrapers[scraper.__name__] = scraper

        return scraper


registry = _ScraperRegistry()
