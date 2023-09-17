import asyncio
import os
import threading
import schedule
import time
from classes.problem_parser import ProblemParser
from classes.save_to_postgre import DBHandler
from dotenv import load_dotenv
from tg_bot.bot import CodeforcesBot

load_dotenv()


def problem_parser_job():
    """Выполняет парсинг заданий и запись их в базу данных."""
    problem_parser = ProblemParser()
    problems_data, problems_stat_data = problem_parser.fetch_data()
    problem_parser.parse(problems_data, problems_stat_data)

    db_handler = DBHandler(os.getenv('PG_CONNECTION'))

    for problem in problem_parser.problems_list:
        db_handler.update_or_add_problem(
            problem['number'],
            problem['name'],
            problem['tags'],
            problem['solved_count'],
            problem['rating'],
            problem['level'],
            problem['url']
        )

    db_handler.close_session()


def bot_worker():
    """Запускает бота в отдельном потоке."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    bot = CodeforcesBot()
    bot.main()


if __name__ == "__main__":
    problem_parser_job()
    schedule.every().hour.do(problem_parser_job)

    bot_thread = threading.Thread(target=bot_worker)
    bot_thread.start()

    while True:
        schedule.run_pending()
        time.sleep(1)
