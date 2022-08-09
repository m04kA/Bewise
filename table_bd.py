import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


def get_db_engine(user="admin", password="root", host="127.0.0.1", port=5433, db_name="bewise_db"):
    url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    if not database_exists(url):
        try:
            create_database(url)
        except sqlalchemy.exc.OperationalError:
            print("Conect error to database")
            exit(1)
    engine = create_engine(url, echo=False)
    return engine


def get_session_db(engine=None):
    if engine is None:
        engine = get_db_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


engine = get_db_engine()
Base = declarative_base()


# Session = sessionmaker(bind=engine)  # Переделать


class Questions(Base):
    """
    Обработать ошибку неправильных (пустых) входных данных для создания (если ляжет внешний сервер)
    """
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


Base.metadata.create_all(engine)

# print(engine)
