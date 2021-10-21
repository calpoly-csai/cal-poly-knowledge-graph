# flask_graphene_mongo/app.py
from tests.local_database import init_db
from flask import Flask, send_from_directory
from flask_graphql import GraphQLView
from schema import schema
from argparse import ArgumentParser

app = Flask(__name__, static_url_path="")
app.debug = True

app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)


@app.route("/visualize")
def display_api():
    return send_from_directory("pages", "voyager.html")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--prod", type=bool, default=False)
    args = parser.parse_args()
    if not args.prod:
        init_db()
    app.run()
