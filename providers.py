from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DbConnect:
    def __init__(self, db_string):
        self.db_string = db_string

    def init_app(self):
        engine = create_engine(self.db_string, echo=False)
        return engine


class SessionManager:
    def __init__(self, db_string):
        self.db_string = db_string
        self.session = None

    def __enter__(self):
        engine = create_engine(
            self.db_string,
            echo=True,
            connect_args={"options": "-c timezone=utc"}
        )
        Session = sessionmaker(bind=engine)
        self.session = Session()
        return self.session

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.session.close()
