from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DBSession = scoped_session(sessionmaker())
Base = declarative_base()


def initialize_db(engine):
    """Initialize sqlite database engine."""
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
