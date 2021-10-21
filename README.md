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

The knowledge graph stays up to date by periodically running web scrapers that grab updated information from external sources. If you want to build your own scraper, the [`CollegeScraper`](./scrapers/college_scraper.py) works as a good example template to get started. All of the scrapers live in the `scrapers` folder. When you run `python app.py`, all scrapers will be loaded and run to populate the database before the API server starts. If you want to run specific scrapers only, you can pass a list of scrapers to the program. For example, `python app.py -s CollegeScraper MusicDepartmentScraper` will only run the college scraper and the music department scraper.

## Visualizing the Knowledge Graph

With the development server running, you can explore a visualization of the Cal Poly Knowledge Graph at [`http://127.0.0.1:5000/visualize`](http://127.0.0.1:5000/visualize).

## Resources

- [BeautifulSoup](https://scribbleghost.net/2020/07/06/getting-started-with-beautiful-soup-4/)
- [AutoScraper](https://github.com/alirezamika/autoscraper)
- [GraphQL + Flask Tutorial](https://graphene-mongo.readthedocs.io/en/latest/tutorial.html)
- [Intro to GraphQL](https://graphql.org/learn/)
- [Learn GraphQL](https://www.howtographql.com)

![Graph Visualization](./docs/assets/graph-visualization.jpg)
