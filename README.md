# BakersParadise

Most recipe sites hand you a huge list of results and leave you to figure out the rest. BakersParadise pulls recipe data from a public API, stores it in a real database, and turns it into something more useful: which recipes are actually beginner-friendly, how long they really take, and which ingredients show up most often. It's built for someone who wants to pick a recipe fast, not spend twenty minutes guessing which one won't be a disaster.

## Features

- Pulls recipe data automatically from [TheMealDB](https://www.themealdb.com/api.php) instead of entering it by hand
- Classifies recipes as beginner-friendly based on ingredient count and prep time
- Buckets recipes by complexity (Low, Medium, High) and by prep time (Quick, Medium, Long)
- Tracks ingredient frequency across the whole dataset
- Two-page Streamlit dashboard: an analytics view for browsing trends, and a recipe explorer for looking at one recipe at a time (image, ingredients, instructions)

## Technologies used

- Python
- SQLite
- Streamlit
- TheMealDB API

## How to run

```bash
cd database
python3 api_data_collection.py
python3 -m streamlit run streamlit_dashboard.py
```

`api_data_collection.py` fetches recipes from the API and saves them to a local SQLite database. `streamlit_dashboard.py` reads from that database and renders the dashboard.

<<<<<<< HEAD
## Design

The project is split into four pieces that each do one job: `api_data_collection.py` pulls and parses recipe data from the API, `data_storage.py` writes it to SQLite, `analysis_logic.py` runs the queries (top ingredients, beginner-friendly recipes, complexity, time categories), and `streamlit_dashboard.py` is the only file that touches the UI. Keeping those separate meant each part could be built and tested on its own.

Beginner-friendly and complexity labels come from a simple, explainable rule (ingredient count and prep time), not a machine learning model. That's a deliberate tradeoff: a rule I can explain in one sentence is something a user can sanity-check for themselves, even if it's less accurate than a more advanced model would be. Prep time itself is estimated with a formula based on ingredient count, not measured from real cooking, and the app is upfront about that so users aren't misled by a number that's really a guess.

A full product write-up, including the tradeoffs, risks, success metrics, and roadmap, is available as part of my portfolio.

## Author

Ja'Leah Beason
