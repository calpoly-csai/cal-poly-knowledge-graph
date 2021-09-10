# Cal Poly Knowledge Graph

A GraphQL API for exploring information about Cal Poly.

## Getting Started

Clone the repository

```bash
git clone https://github.com/calpoly-csai/cal-poly-knowledge-graph.git
```

Set up the development environment

```bash
conda env create --file environment.yml
pre-commit install
```

Launch the development server

```bash
python app.py
```

Visit [`http://127.0.0.1:5000/graphql`](http://127.0.0.1:5000/graphql) in your browser to interact with the API. For more information about the GraphiQL UI, check out the [docs](https://github.com/graphql/graphiql/tree/main/packages/graphiql#readme)

## Resources

- [GraphQL + Flask Tutorial](https://graphene-mongo.readthedocs.io/en/latest/tutorial.html)
- [Intro to GraphQL](https://graphql.org/learn/)
- [Learn GraphQL](https://www.howtographql.com)

![test](./docs/assets/graph-visualization.jpg)
