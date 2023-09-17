from classes.problem_parser import Problem, ProblemStatistics, ProblemParser


def test_problem_to_dict():
    problem = Problem(1, 'A', 'Problem A', ['tag1', 'tag2'], 1000)
    result = problem.to_dict()
    assert result == {
        'number': '1A',
        'name': 'Problem A',
        'tags': 'tag1, tag2',
        'rating': 1000,
        'level': 'Easy',
        'url': 'https://codeforces.com/problemset/problem/1/A'
    }


def test_problem_statistics_to_dict():
    problem_stat = ProblemStatistics(1, 'A', 50)
    result = problem_stat.to_dict()
    assert result == {
        'number': '1A',
        'solved_count': 50
    }


def test_problem_parser():
    parser = ProblemParser()
    problems_data = [
        {
            'contestId': 1,
            'index': 'A',
            'name': 'Problem A',
            'tags': ['tag1', 'tag2'],
            'rating': 1000
        }
    ]
    problems_stat_data = [{'contestId': 1, 'index': 'A', 'solvedCount': 50}]
    parser.parse(problems_data, problems_stat_data)
    assert len(parser.problems_list) == 1
    assert parser.problems_list[0]['name'] == 'Problem A'


def test_determination_level():
    """Проверяем аргументы"""
    assert Problem.determination_level(500) == 'Easy'
    assert Problem.determination_level(1500) == 'Middle'
    assert Problem.determination_level(2500) == 'Hard'
