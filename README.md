# sample_py_api
Sample Python API with live endpoints, DB configuration, and DB fill logic.

## Setup ##
This app assumes that postgres is installed on the system. I used Poetry to handle packages, but that's not required.

## Endpoints ##
Run app (poetry run start) and refer to http://127.0.0.1/docs

## TODO ##
- Add tests
  - Unit testing: parsing logic, API endpoint logic
  - Integration testing: API connection
- Improve get by name logic
  - Multiple heroes have the same alias (2 Batmans for example), and the delete/update logic need to be adjusted to handle that.

## Personal Notes ##
- I prefer straight SQL when possible, but SQLAlchemy seemed like a better fit in this case since it handles DB and table creation.
- I generally prefer not writing in OOP style for Data Engineering work (my Airflow DAGs for example usually don't have class models unless that is the team preference)
