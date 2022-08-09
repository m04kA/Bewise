import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from loguru import logger


def get_db_engine(user="admin", password="root", host="127.0.0.1", port=5433, db_name="bewise_db"):
    logger.debug(
        f"Create url to database:\nUser = {user};\nPassword = {password};\nHost = {host};\nPort = {port};\n"
        f"DB name = {db_name};")
    url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    if not database_exists(url):
        logger.info(f"Database {db_name} not exists. Create new database.")
        try:
            create_database(url)
            logger.info(f"Database {db_name} created.")
        except sqlalchemy.exc.OperationalError:
            logger.error(f"Connection to database {db_name} failed.")
            exit(1)

    logger.info(f"Create engine to database {db_name}.\nUrl = {url}.")
    engine = create_engine(url, echo=False)
    return engine


def get_session_db(engine=None):
    logger.debug(f"Start creating session to database.")
    if engine is None:
        logger.info(f"Engine is None. Get new engine to DB.")
        engine = get_db_engine()
    logger.info(f"Create session to database.")
    Session = sessionmaker(bind=engine)
    session = Session()
    logger.debug(f"Session to database created.\nSession = {session}.")
    return session


engine = get_db_engine()
Base = declarative_base()


class Questions(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    question = Column(String(500), nullable=False)
    answer = Column(String(250), nullable=False)
    created_at = Column(DateTime)

    def __init__(self, id, question, answer, created_at):
        self.id = id
        self.question = question
        self.answer = answer
        self.created_at = created_at

    def __repr__(self):
        return f"<Questions {self.question}>"


logger.debug(f"Create table {Questions.__tablename__}.")
Base.metadata.create_all(engine)
