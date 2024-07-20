# CRON-Fetch-Event

## Introduction 📌
Welcome to Python Cron Fetch Event! </br>
This Cron job fetches the data from third party api ```https://provider.code-challenge.feverup.com/api/events``` at store the events which are online in <strong> Postgres SQL </strong> database.

## Requirements 🏁

* [Python](https://www.python.org/)

## How to run locally

Below are steps to run the api.

- Clone the repository using below command:

```bash
git clone git@github.com:nitinNinjatech/events-fetch-api.git 
```

- Enter into the new directory:

```bash
cd cron-fetch-event
```

- Create the virtual Environment using below command

```
python -m venv venv
```

- Activate the virtual environment
```
venv\Scripts\activate
```

- Install dependecies
```
python -m pip install -r requirements.txt
```

- Create ```.env``` file in the root directory of project with below values
```
PROVIDER_API=https://provider.code-challenge.feverup.com/api/events
DATABSE_NAME=events_db
DATABASE_USER=postgres
DATABASE_PASS=pgadmin
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

- Run the make command. It will initialize the database and fetch one time events from api
```
make run
```

- To continuously fetch the data and store in database use either ```crontab``` in linux or task scheduler
  to fetch events.
  
