from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base


load_dotenv()

Base = declarative_base()


class ProblemDB(Base):
    """
    Модель для представления данных о задачах в базе данных.
    """
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True)
    number = Column(String, unique=True)
    name = Column(String)
    tags = Column(String)
    solved_count = Column(Integer)
    rating = Column(Integer)
    level = Column(String)
    url = Column(String)

    def __repr__(self):
        return f"<Problem(number='{self.number}'," \
               f" name='{self.name}', tags='{self.tags}'," \
               f" solved_count={self.solved_count}, rating={self.rating}, " \
               f"level={self.level}, url={self.url})>"


class DBHandler:
    """
    Обработчик взаимодействия с базой данных для сущностей Problem.
    """
    def __init__(self, db_url):
        """
        Инициализация DBHandler.
        """
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def update_or_add_problem(self, number, name, tags,
                              solved_count, rating, level, url):
        """
        Обновляет или добавляет задачу в базу данных.
        """
        existing_problem = self.get_problem_by_number(number)
        if existing_problem:
            if (existing_problem.name != name or
                    existing_problem.tags != tags or
                    existing_problem.solved_count != solved_count or
                    existing_problem.rating != rating or
                    existing_problem.level != level or
                    existing_problem.url != url):
                existing_problem.name = name
                existing_problem.tags = tags
                existing_problem.solved_count = solved_count
                existing_problem.rating = rating
                existing_problem.level = level
                existing_problem.url = url

                self.session.commit()
                print(f"Обновлена задача: {number}")
            else:
                print(f"Задача {number} уже существует и атрибуты не"
                      f" изменились")
        else:
            problem = ProblemDB(number=number, name=name,
                                tags=tags, solved_count=solved_count,
                                rating=rating, level=level, url=url)
            self.session.add(problem)
            self.session.commit()
            print(f"Добавлена новая задача: {number}")

    def get_problem_by_number(self, number):
        """
        Извлекает задачу по её уникальному номеру.
        """
        return self.session.query(ProblemDB).filter(
            ProblemDB.number == number
        ).first()

    def close_session(self):
        """
        Закрывает сессию базы данных.
        """
        self.session.close()
