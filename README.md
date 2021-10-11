# Cal Poly Knowledge Graph

A GraphQL API for exploring information about Cal Poly.

## Getting Started

Clone the repository

```bash
git clone https://github.com/calpoly-csai/cal-poly-knowledge-graph.git
```

Set up the development environment. Run these commands at the root of the `cal-poly-knowledge-graph` folder.

```bash
conda env create --file environment.yml
conda activate cp-knowledge-graph
pre-commit install
```

Launch the development server

```bash
python app.py
```

Visit [`http://127.0.0.1:5000/graphql`](http://127.0.0.1:5000/graphql) in your browser to interact with the API. For more information about how to query data using GraphQL, check out the [docs](https://graphql.org/learn/queries/). Visit the web scrapers section to get started with development.

## Web Scrapers

The knowledge graph stays up to date by periodically running web scrapers that grab updated information from external sources. You can run these web scrapers by calling `python scrape_data.py`. To write your own web scraper, add a new Python file to the `scrapers` directory. The [`CollegeScraper`](./scrapers/college_scraper.py) works as a good example template to get started.

## Resources

- [BeautifulSoup](https://scribbleghost.net/2020/07/06/getting-started-with-beautiful-soup-4/)
- [AutoScraper](https://github.com/alirezamika/autoscraper)
- [GraphQL + Flask Tutorial](https://graphene-mongo.readthedocs.io/en/latest/tutorial.html)
- [Intro to GraphQL](https://graphql.org/learn/)
- [Learn GraphQL](https://www.howtographql.com)

![Graph Visualization](./docs/assets/graph-visualization.jpg)
