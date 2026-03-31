# Python Data Platform Boilerplate

A generic, lightweight data governance and dashboard platform written purely in Python and Streamlit. This repository is modeled after standard data platform architectures (similar to dbt) and provides a clean boilerplate starting point for your next data project.

## Features

- **Layered Architecture**: Native support for standard data modeling layers (`staging`, `intermediate`, `marts`, `exposures`).
- **Data Catalog & Discovery**: Auto-generating data catalog (`helpers/utilities/model_catalog.py`) that indexes and surfaces your Python models dynamically in the UI.
- **Sample Datasets Included**: Pre-configured with standard dummy datasets (`jaffle_shop`, `payments`) to showcase table relationships, dimensions, and facts.
- **Built-in UI Dashboards**: Fast, interactive executive dashboard powered by Streamlit and Plotly.

## Project Structure

- `models/`: The core data logic separated into distinct modeling layers.
- `helpers/`: Vital UI components and catalog-building utilities.
- `pages/`: Streamlit view routing for Reports, Tools (like the Data Catalog), and Dev environments.
- `guides/`: Boilerplate guidelines detailing folder structure, deployment, and naming conventions.

## Quickstart

Check out the explicit local setup guide in [guides/how_set_up_local_env.md](guides/how_set_up_local_env.md).

Alternatively, assuming Python 3 is installed:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deployment

Deploy updates via the `scripts/release.sh` workflow or see [`guides/deploy_cloud.md`](guides/deploy_cloud.md) for deeper integrations with Google Cloud and AWS.
