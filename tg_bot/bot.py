import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hlink
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup
from funcs.queries_to_db import get_problems_data, get_problems_topics, get_search_data
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from dotenv import load_dotenv

load_dotenv()


class Search(StatesGroup):
    """Стейты для поиска."""
    Find = State()


class CodeforcesBot:
    """Бот для работы с задачами Codeforces."""
    def __init__(self):
        """Инициализация бота."""
        self.bot = Bot(token=os.getenv('TG_API_TOKEN'), parse_mode=types.ParseMode.HTML)
        self.storage = MemoryStorage()
        self.dp = Dispatcher(self.bot, storage=self.storage)

        # Регистрация обработчиков
        self.dp.register_message_handler(self.start, commands='start')
        self.dp.register_message_handler(self.find_command, commands='find', state=None)
        self.dp.register_message_handler(self.find_problems, state=Search.Find)
        self.dp.register_message_handler(self.handle_difficulty_choice,
                                         lambda message: message.text in ['Easy', 'Middle', 'Hard'])
        self.dp.register_message_handler(self.get_problems_cards,
                                         lambda message: message.text in get_problems_topics())

    async def on_shutdown(self, dp):
        """Закрытие бота при завершении работы."""
        await self.bot.close()
        await self.storage.close()

    async def start(self, message: types.Message):
        """Обработка команды /start."""
        level_buttons = ['Easy', 'Middle', 'Hard']
        level_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(*level_buttons)

        await message.answer('Выберите уровень сложности, {0.first_name}'.format(message.from_user),
                             reply_markup=level_menu)

    async def find_command(self, message: types.Message):
        """Обработка команды /find."""
        await message.answer("Введите полное или частичное название задачи: ")
        await Search.Find.set()

    async def find_problems(self, message: types.Message, state: FSMContext):
        """Поиск задач по названию."""
        answer = message.text
        await state.update_data(answer1=answer)
        await message.answer('Processing...')

        if message.text:
            problems_data = get_search_data(message.text)
            try:
                for problem in problems_data:
                    card = f"{hlink(problem[1], problem[4])}\n" \
                           f"{hbold('Номер: ')}{problem[0]}\n" \
                           f"{hbold('Тема: ')}{problem[2]}\n" \
                           f"{hbold('Сложность: ')}{problem[6]}\n" \
                           f"{hbold('Решения: ')}{problem[5]}\n"
                    await message.answer(card)
            except Exception as e:
                await message.answer(f'Произошла ошибка: {e}')

        await state.finish()

    async def handle_difficulty_choice(self, message: types.Message, state: FSMContext):
        """Обработка выбора уровня сложности."""
        problems_topics = get_problems_topics()
        problems_topics_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(*problems_topics)

        user_choice = message.text
        await message.answer(f'Вы выбрали уровень сложности: {user_choice}! Теперь выберете тему.',
                             reply_markup=problems_topics_menu)
        await state.update_data(selected_level=user_choice)

    async def get_problems_cards(self, message: types.Message, state: FSMContext):
        """Отправка карточек задач пользователю."""
        problems_topics = get_problems_topics()
        problems_menu = ReplyKeyboardMarkup(resize_keyboard=True)

        for topic in problems_topics:
            problems_menu.add(topic)

        async with state.proxy() as data:
            level_input = data.get("selected_level")

        theme_input = message.text
        problems_data = get_problems_data(theme=theme_input, level=level_input)

        problems_menu.keyboard.clear()

        for problem in problems_data:
            card = f"{hlink(problem[1], problem[4])}\n" \
                   f"{hbold('Номер: ')}{problem[0]}\n" \
                   f"{hbold('Тема: ')}{problem[2]}\n" \
                   f"{hbold('Сложность: ')}{problem[6]}\n" \
                   f"{hbold('Решения: ')}{problem[5]}\n"

            await self.bot.send_message(message.from_user.id, card, reply_markup=problems_menu)

    def main(self):
        """Запуск бота."""
        executor.start_polling(self.dp, on_shutdown=self.on_shutdown)
