# Hotel_API
Generic Hotel API for a basic hotel administrations system created with FastAPI and PostgreSQL to simplify and structure hotel operations.


## Table Of Contents

1. [General info](general-info.md)
2. [Database design](HotelAPI_db.md)
3. [Installation](installation.md)
4. [Routers overview](overview.md)
5. [How-To Guides](how-to-guides.md)

## Project Overview

Features

    Create different types of room with own price and fixtures.
    Store and search information about guests, bookings and hotel facilities.
    Create Bookings depending on the room state (free or booked).
    Check if booking's payment is full, if guest has any open requests.
    Role based access to functionality (Admin/User).


Getting Started

    Setup database (heroku-postgresql hobby-dev is a great free option)
    Add database URL to .env file
    Setup keys in .env file as per need.
    Setup a local environment
    Update database via migrations
    Start app and create first user (admin)


## Project layout

    db.py            # Config files for database connection
    main.py          # Main executable file
    mkdocs.yml       # The configuration file for mkdocs.
    requirements.txt # File with dependencies
    docs/
        index.md     # The documentation homepage.
        ...          # Other markdown pages, images and other files.
    crud/
        rooms.py     # Modules to work with database's models "rooom"
        ...          # Other modules to work with similar models in database
    migration/
        version/     # Folder with transaction to prepare tables in database
        env.py       # Alembic Config object
        ...          # Other files for Alembic
    models/
        room.py      # Database models with information about room
        ...          # Other modelues with db models
    routers/
        room.py      # Endpoints for rooms functionality
        ...          # Other modules for endpointes
    schemas/
        room.py      # Pydantic schemas for rooms models
        ...          # Other files with pydantic schemas
    tests/
        room.py      # Tests for room logic
        ...          # Other tests for whole api
    utils/
        users.py     # Helper functions for auth logic
