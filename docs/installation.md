* #### Create a virtual environment.

`python -m venv .\venv`

* #### Activate it.

`.\venv\Scripts\activate.bat`

* #### Install dependencies.

`pip install -r requirements.txt`

* #### Preparing the database.

`alembic upgrade head`

* #### Start the service.

`uvicorn main:app --host 0.0.0.0 --port 8001`
