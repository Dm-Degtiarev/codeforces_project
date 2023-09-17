from classes.save_to_postgre import DBHandler
from dotenv import load_dotenv
import os

load_dotenv()


def test_db_handler_update_or_add_problem():
    db_handler = DBHandler(os.getenv('PG_CONNECTION'))
    number = '1A'
    name = 'Problem A'
    tags = 'tag1, tag2'
    solved_count = 50
    rating = 1000
    level = 'Easy'
    url = 'https://codeforces.com/problemset/problem/1/A'

    db_handler.update_or_add_problem(number, name, tags,
                                     solved_count, rating, level, url)

    problem = db_handler.get_problem_by_number(number)
    assert problem is not None
    assert problem.number == number
    assert problem.name == name
    assert problem.tags == tags
    assert problem.solved_count == solved_count
    assert problem.rating == rating
    assert problem.level == level
    assert problem.url == url


def test_db_handler_get_problem_by_number():
    db_handler = DBHandler(os.getenv('PG_CONNECTION'))
    number = '1B'
    name = 'Problem B'
    tags = 'tag3, tag4'
    solved_count = 100
    rating = 1200
    level = 'Medium'
    url = 'https://codeforces.com/problemset/problem/1/B'

    db_handler.update_or_add_problem(number, name, tags,
                                     solved_count, rating, level, url)

    problem = db_handler.get_problem_by_number(number)
    assert problem is not None
    assert problem.number == number
    assert problem.name == name
    assert problem.tags == tags
    assert problem.solved_count == solved_count
    assert problem.rating == rating
    assert problem.level == level
    assert problem.url == url
