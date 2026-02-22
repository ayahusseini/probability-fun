# Probability Fun

A project to develop **intuition for probability** through Python simulations and Monte Carlo experiments.

## Monte Carlo ?

From [the ELI5 subreddit](https://www.reddit.com/r/explainlikeimfive/comments/1cfsoyu/comment/l1r6aql/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button)

>Basically, it’s a way for computers to estimate the answer to a mathematical problem by taking a bunch of random samples. 

>For example, lets say you wanted to figure out the area of a circle. What you would do is draw a square around the circle that touches the edges and generate random points in that square. For each point, you calculate whether it is in the circle or not and then count the ones that are in the circle and not in the circle. If you generate enough samples, you should get that about 78.5% of the points are in the circle, so you can estimate that the area of the circle is 78.5% the area of the square


# Setup 

Reccomended setup is through [uv](https://docs.astral.sh/uv/getting-started/installation/). 

## Quick Start (using notebooks)

If you just want to use `notebooks/` to explore problems

```sh
uv sync
```

You do not need the dev setup if you aren't intending to change `src/` code 

Alternatively, you can set up using `pip`:

```sh
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -e .
```

## Development setup 

If you plan to modify code, run tests, or commit changes:

1. Install dependencies 

```sh
uv sync
```

2. Install [pre-commit hooks](https://pre-commit.com/)

```sh
uv run pre-commit install
```

These enforce:
- Formatting via Ruff
- Lockfile validation via uv
- Shell + workflow checks

3. Run tests via

```sh
uv run pytest
```

## Files and Folders

```
── notebooks
├── pyproject.toml
├── README.md
├── src
│   └── probability_simulator
│       ├── __init__.py
│       ├── coin_flips.py
│       └── tests
└── uv.lock
```

### Directory structure
- `src/`: This is the build path
    - `probability_simulator`: A package containing most simulation code
- `notebooks/`: Jupyter notebooks demonstrating simulations, comparing Monte Carlo results to theoretical solutions.
