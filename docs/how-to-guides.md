## Migrations

You can also run the migrations with alembic commands to prepare database.

### Update database

* Make sure you create a "revision" of your models and that you "upgrade" your database with that revision every time you change them. As this is what will update the tables in your database.

```
alembic revision --autogenerate -m "Update required tables"
```
* After creating the revision, run the migration in the database (this is what will actually change the database):
```
alembic upgrade head
```