# Newton Benchmarks Dashboard

This repository aggregates and publishes the benchmark results for the [Newton](https://github.com/newton-physics/newton) physics engine.
The benchmark data is collected using [airspeed velocity (`asv`)](https://asv.readthedocs.io/en/latest/).

**View the live dashboard:** **[newton-physics.github.io/newton-asv/](https://newton-physics.github.io/newton-asv/)**

This repository is only used for aggregating results and publishing the `asv` dashboard.
The `asv run` command is not meant to be executed from this repository.

## How It Works

1. The benchmarks themselves reside in the [main Newton repository](https://github.com/newton-physics/newton/tree/main/asv/benchmarks).
2. Automation runs the `asv` benchmarks against new commits.
3. The raw results are then pushed to the `main` branch of *this* repository.
4. A GitHub Actions workflow here takes the new results and uses the `asv gh-pages` command to update and publish the web dashboard.

## Local Testing

First, install `asv` in your local Python environment:

```
pip install asv
```

Then generate the web dashboard and start a local web server to preview the results:

```
asv publish
asv preview --browser
```
