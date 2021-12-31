import pytest
from scrape_data import scrape_data
from local_database import start_db
from graphene.test import Client
from schema import schema
from typing import Callable, Union, Any, List


def tree_map(
    f: Callable[[Union[str, int, float]], Any], query_result: Union[dict, list]
) -> List[Any]:
    """
    Runs the provided function on the leaves of `query_result`
    """
    if type(query_result) in [dict, list]:
        results = []
        sub_query = (
            query_result.values() if type(query_result) == dict else iter(query_result)
        )
        for query in sub_query:
            results += tree_map(f, query)
        return results
    else:
        return [f(query_result)]


@pytest.fixture(scope="module")
def client():
    start_db()
    return Client(schema)


def test_run(client):
    """
    Ensure that all scrapers run.
    """
    scrape_data()


def test_college_scraper(client):
    """Ensures that the college scraper populates the database with an example"""
    scrape_data(["CollegeScraper"])
    result = client.execute(
        """
    query {
    college(name: "Engineering") {
        edges {
        node {
            departments(name: "Computer Science") {
            edges {
                node {
                name
                }
            }
            }
        }
        }
    }
    }
    """
    )
    # Ensure the query returned a department with the name "Computer Science"
    is_cs = lambda v: type(v) == str and v == "Computer Science"
    assert any(tree_map(is_cs, result))
