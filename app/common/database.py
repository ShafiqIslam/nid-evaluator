
from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from app.config import DB
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

engine = create_engine(DB.to_string(), convert_unicode=True,pool_size=100,pool_pre_ping=True,pool_recycle=280)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
db = SQLAlchemy()
migrate = Migrate()


class CustomBase(object):
    """This overrides the default
    `_declarative_constructor` constructor.
    It skips the attributes that are not present
    for the model, thus if a dict is passed with some
    unknown attributes for the model on creation,
    it won't complain for `unkwnown field`s.
    """

    def __init__(self, **kwargs):
        cls_ = type(self)
        for k in kwargs:
            if hasattr(cls_, k):
                setattr(self, k, kwargs[k])
            else:
                continue

    """
    Set default tablename
    """

    @declared_attr
    def __tablename__(self, cls):
        return cls.__name__.lower()

    """
    Add and try to flush.
    """

    def save(self):
        db_session.add(self)
        self._flush()
        return self

    """
    Update and try to flush.
    """

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
        return self.save()

    """
    Delete and try to flush.
    """

    def delete(self):
        db_session.delete(self)
        self._flush()

    """
    Try to flush. If an error is raised,
    the session is rollbacked.
    """

    def _flush(self):
        try:
            db_session.flush()
        except DatabaseError:
            db_session.rollback()


BaseModel = declarative_base(cls=CustomBase, constructor=None)
BaseModel.query = db_session.query_property()
BaseModel.base_query = db_session.query

from app.models import *


def init_db(application):
    """
    Create database if doesn't exist and
    create all tables.
    """
    if not database_exists(engine.url):
        create_database(engine.url)
    # BaseModel.metadata.create_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)
    application.config['SQLALCHEMY_DATABASE_URI'] = DB.to_string()
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(application)
    migrate.init_app(application, db)


def drop_db():
    """
    Drop all of the record from tables and the tables
    themselves.
    Drop the database as well.
    """
    BaseModel.metadata.drop_all(bind=engine)
    drop_database(engine.url)
