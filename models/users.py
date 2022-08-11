import sqlalchemy

metadata = sqlalchemy.MetaData()


user = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(40), unique=True, index=True),
    sqlalchemy.Column("name", sqlalchemy.String(100)),
    sqlalchemy.Column("hashed_password", sqlalchemy.String()),
    sqlalchemy.Column(
        "is_active",
        sqlalchemy.Boolean(),
        server_default=sqlalchemy.sql.expression.true(),
        nullable=False,
    ),
    sqlalchemy.Column(
        "is_admin",
        sqlalchemy.Boolean(),
        server_default=sqlalchemy.sql.expression.false(),
        nullable=False,
    ),
)
