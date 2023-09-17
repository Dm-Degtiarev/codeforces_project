import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes.save_to_postgre import ProblemDB
from funcs.queries_to_db import get_problems_data, get_search_data


def test_get_problems_data():
    engine = create_engine(os.getenv('PG_CONNECTION'))
    Session = sessionmaker(bind=engine)
    session = Session()

    # Вставляем данные
    theme = 'test'
    level = 'test'
    for _ in range(10):
        problem = ProblemDB(tags=theme, level=level, rating=1000)
        session.add(problem)

    session.commit()

    # Тестируем функцию
    problems = get_problems_data(theme, level)

    assert len(problems) == 10
    assert all(p.tags == theme and p.level == level for p in problems)


def test_get_search_data():
    engine = create_engine(os.getenv('PG_CONNECTION'))
    Session = sessionmaker(bind=engine)
    session = Session()

    # Вставляем данные
    problem_name = 'Test Problem'
    for _ in range(10):
        problem = ProblemDB(name=problem_name, rating=1000)
        session.add(problem)
    session.commit()

    # Тестируем функцию
    problems = get_search_data(problem_name)

    assert len(problems) == 10
    assert all(p.name.lower() in problem_name.lower() for p in problems)
