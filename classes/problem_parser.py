import requests
from abc import ABC, abstractmethod


class ProblemBase(ABC):
    """Абстрактный базовый класс для задач и статистики задач."""
    __slots__ = ()

    @abstractmethod
    def to_dict(self):
        """Преобразует данные в словарь."""
        pass


class Problem(ProblemBase):
    """Класс, представляющий задачу."""
    __slots__ = ('contest_id', 'index', 'name', 'tags', 'rating')

    def __init__(self, contest_id, index, name, tags, rating):
        """
        Инициализация объекта задачи.
        Args:
            contest_id (int): ID соревнования.
            index (str): Индекс задачи.
            name (str): Название задачи.
            tags (list): Список тегов задачи.
            rating (int): Сложность
        """
        self.contest_id = contest_id
        self.index = index
        self.name = name
        self.tags = tags
        self.rating = rating

    def to_dict(self):
        """Преобразует данные в словарь."""
        return {
            'number': f"{self.contest_id}{self.index}",
            'name': self.name,
            'tags': ', '.join(self.tags),
            'rating': self.rating,
            'level': self.determination_level(self.rating),
            'url': f"https://codeforces.com/problemset/problem/"
                   f"{self.contest_id}/{self.index}"
        }

    @staticmethod
    def determination_level(arg):
        """Определяет уровень сложности задачи"""
        if arg is None:
            return None
        elif arg <= 1000:
            return 'Easy'
        elif arg <= 2000:
            return 'Middle'
        else:
            return 'Hard'


class ProblemStatistics(ProblemBase):
    """Класс, представляющий статистику задачи."""
    __slots__ = ('contest_id', 'index', 'solved_count')

    def __init__(self, contest_id, index, solved_count):
        """
        Инициализация объекта статистики задачи.
        Args:
            contest_id (int): ID соревнования.
            index (str): Индекс задачи.
            solved_count (int): Количество решивших задачу.
        """
        self.contest_id = contest_id
        self.index = index
        self.solved_count = solved_count

    def to_dict(self):
        """
        Преобразует данные в словарь.
        """
        return {
            'number': f"{self.contest_id}{self.index}",
            'solved_count': self.solved_count
        }


class ProblemParser:
    """Класс для парсинга данных о задачах."""
    def __init__(self):
        """Инициализация парсера задач."""
        self.problems_list = []

    def fetch_data(self):
        """
        Получает данные о задачах с Codeforces API.
        """
        response = requests.get(
            "https://codeforces.com/api/problemset.problems"
        ).json()
        problems = response['result']['problems']
        problems_statistics = response['result']['problemStatistics']

        return problems, problems_statistics

    def parse(self, problems, problems_statistics):
        """
        Парсит данные о задачах и их статистике.
        """
        for problem, problem_statistic in zip(problems, problems_statistics):
            contest_id = problem['contestId']
            index = problem['index']
            name = problem['name']
            tags = problem['tags']
            solved_count = problem_statistic['solvedCount']

            points = problem.get('rating')
            problem_obj = Problem(contest_id, index, name, tags, points)
            problem_stat_obj = ProblemStatistics(
                contest_id,
                index,
                solved_count
            )

            self.problems_list.append({
                **problem_obj.to_dict(),
                **problem_stat_obj.to_dict()
            })
