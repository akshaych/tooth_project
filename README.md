# The Tooth Project

The tooth project is a Flask application that sets up a local database and flask server to
add and retrieve events all things toothy!

## Installation and Set Up

https://direnv.net/docs/installation.html
 -- follow this tutorial to install direnv (a shell extension that manages your environment variables)

Then run ```poetry install``` in the home directory of this project -- all dependencies
are managed through poetry.

Set the following env variables in your .envrc file in the home directory of this project
```commandline
export FLASK_APP=***
export JWT_SECRET_KEY=***
export FLASK_ENV=***
export SQLALCHEMY_DATABASE_URI=***
```
Finally, run ```poetry run flask run``` to get the server running!

## Usage

This project uses JWT tokens to authenticate -- you must first retrieve 
an appropriate JWT token using the ```token``` endpoint. After that, feel free to use the ```get_events``` or
```add_event``` endpoints.

```get_events``` takes in (optionally) start_dt, end_dt, event_type, event_level and verbose parameters. 
The first four are self-explanatory and the verbose option allows you to return the name form of the 
enums that exist in the db, instead of the numerical enum value. 

```add_event``` takes in (optionally) dt, event_type, event_level, metadata_json and tooth_id as parameters.
If a tooth_id is passed in, that will automatically map to a tooth_type enum that is also stored in the events table.

