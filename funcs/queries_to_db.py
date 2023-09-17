import os
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from classes.save_to_postgre import ProblemDB
from dotenv import load_dotenv

load_dotenv()


def get_problems_topics():
    """
    Получает список тем задач, удовлетворяющих условиям.

    Returns:
        list: Список тегов задач.
    """
    engine = create_engine(os.getenv('PG_CONNECTION'))

    # Создаем сессию
    Session = sessionmaker(bind=engine)
    session = Session()

    # Формируем запрос
    tags_query = (
        session.query(ProblemDB.tags)
        .filter(
            ProblemDB.tags.notilike('%,%'),
            ProblemDB.tags != '',
            ProblemDB.rating.isnot(None)
        )
        .group_by(ProblemDB.tags)
        .having(func.count().op('>=')(10))
    )

    tags_list = [result[0] for result in tags_query]
    session.close()

    return tags_list


def get_problems_data(theme, level):
    """
    Получает данные о задачах по указанной теме и уровню сложности.
    """
    engine = create_engine(os.getenv('PG_CONNECTION'))

    Session = sessionmaker(bind=engine)
    session = Session()

    tags_query = (
        session.query(ProblemDB.number,
                      ProblemDB.name,
                      ProblemDB.tags,
                      ProblemDB.rating,
                      ProblemDB.url,
                      ProblemDB.solved_count,
                      ProblemDB.level
                      )
        .filter(
            ProblemDB.rating.isnot(None),
            ProblemDB.tags == theme,
            ProblemDB.level == level,
        )
        .order_by(func.random())
        .limit(10)
    ).all()

    session.close()

    return tags_query


def get_search_data(problem_name):
    """
    Поиск задачи по частичному или полному совпадению названия.

    Args:
        problem_name (str): Название задачи.
    Returns:
        list: Список данных о задачах.
    """
    engine = create_engine(os.getenv('PG_CONNECTION'))

    Session = sessionmaker(bind=engine)
    session = Session()

    tags_query = (
        session.query(
            ProblemDB.number,
            ProblemDB.name,
            ProblemDB.tags,
            ProblemDB.rating,
            ProblemDB.url,
            ProblemDB.solved_count,
            ProblemDB.level
        )
        .filter(
            ProblemDB.rating.isnot(None),
            ProblemDB.name.ilike(f'%{problem_name}%')
        )
        .order_by(func.random())
        .limit(10)
    ).all()
    session.close()

    return tags_query
