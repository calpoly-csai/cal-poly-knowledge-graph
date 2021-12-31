"""
Top-level code for launching the CP Knowledge Graph server
"""
from local_database import populate_db, start_db
from flask import Flask, send_from_directory
from flask_graphql import GraphQLView
from schema import schema
from argparse import ArgumentParser
from scrape_data import scrape_data

app = Flask(__name__, static_url_path="")
app.debug = True

app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)


@app.route("/visualize")
def display_api():
    """
    Displays the GraphQL Voyager page that allows users to visually explore the API
    """
    return send_from_directory("pages", "voyager.html")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--prod", type=bool, default=False)
    parser.add_argument("--scrapers", "-s", nargs="*", default=[])
    args = parser.parse_args()
    if not args.prod:
        start_db()
        populate_db()
        scrape_data(args.scrapers)
    app.run()
