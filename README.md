# Hotel_API
API for Hotel administrations via FastAPI.

This project serves a simple hotel administrations system API that includes the following aspects (CRUD):

    * room categories can be created, viewed, updated, deleted and modified with features
    * rooms can be created, viewed, updated, and deleted
    * guests can be created, viewed, updated, and deleted
    * bookings can be created, viewed, updated, and deleted
    * payments can be created, viewed, updated, and deleted
    * requests can be created, viewed, updated, and deleted
    * users can be created, viewed, updated, and deleted by admins

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
    utils/
        users.py     # Helper functions for auth logic
