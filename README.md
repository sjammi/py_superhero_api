# sample_py_api
Sample Python API with live endpoints, DB configuration, and DB fill logic.

## Setup ##
This app assumes that Postgres and Python 3.9 are installed on the system. I used Poetry to handle packages, but that's not required.
Run `poetry run setup` to create the local DB and fill it from the Superheroes API (https://akabab.github.io/superhero-api/api). Run `poetry run start` to start up the API.

## Database ##
Models and indexes can be found in [db.py](/superheroes/utils/db.py)
![Alt text](/screenshots/api_docs.png?raw=true)

## Endpoints ##
Run app and refer to `http://localhost:8000/docs` / `http://localhost:8000/redoc` for full details.
![Alt text](/screenshots/api_docs.png?raw=true)

## TODO ##
- Add tests
  - Unit testing: parsing logic, API endpoint logic
  - Integration testing: API connection
- Improve get by name logic
  - Multiple heroes have the same alias (2 Batmans for example), and the delete/update logic needs to be adjusted to handle that.

## Personal Notes ##
- I prefer straight SQL when possible, but SQLAlchemy seemed like a better fit in this case since it handles DB and table creation.
- I usually prefer not writing in OOP style for Data Engineering work (my Airflow DAGs for example usually don't have classes unless that is the team preference)
- Could add `pg_trgm` to improve performance on the `ilike` queries
- This project runs in python 3.9, but I believe it can work on a lower version aside from the method `HeroParser.parse_hero_stats`

## Screenshots ##
![Alt text](/screenshots/hero_db.png?raw=true "Hero DB sample")
![Alt text](/screenshots/get_hero.png?raw=true "Get hero")
![Alt text](/screenshots/get_strongest.png?raw=true "Get strongest by stat")
![Alt text](/screenshots/get_team.png?raw=true "Get single team")
![Alt text](/screenshots/get_team_fuzzy.png?raw=true "Get all teams fuzzy search")
![Alt text](/screenshots/update_successful.png?raw=true "Update hero description")
![Alt text](/screenshots/update_stats_successful.png?raw=true "Update stats")
![Alt text](/screenshots/sample_error.png?raw=true "All errors return in the same format")


Any and all feedback is welcome!
