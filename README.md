# codeforces_project

## Описание

Проект представляет собой backend приложение, которое собирает/обновляет данные по задачам на сайте https://codeforces.com/problemset в БД (СУБД: PostgreSQL).

Далее, на эти данные подключается Telegram-bot, в котором задается уровень сложности (rating <= 1000 - Easy, 1000 < rating <= 2000 - Middle, rating > 2000 - Hard): 
![image](https://github.com/Dm-Degtiarev/codeforces_project/assets/123110865/f4339996-fc82-48dd-a0c7-310de6d068a8)


с последующим выбором контеста (Набор задач по теме):
![image](https://github.com/Dm-Degtiarev/codeforces_project/assets/123110865/41b02ce0-d107-427d-905e-3f5e596c7ae3)

и выводом 10 карточек случайных задач в рамках выбранного контеста:
![image](https://github.com/Dm-Degtiarev/codeforces_project/assets/123110865/7e45b2c9-7d52-47f5-9570-8c1b8d0ae80b)

Так же в боте предусмотрен поиск задач по названию/частичному названию. Для этого используется команда /find с последующим вводом от пользователя текста по которому будет происходить поиск:
![image](https://github.com/Dm-Degtiarev/codeforces_project/assets/123110865/3e16b9f0-2072-413f-9f72-3ca0d249d68b)

Пример вывода:
![image](https://github.com/Dm-Degtiarev/codeforces_project/assets/123110865/f86a3d07-7d6f-4df9-ade3-fe0414cab8df)

Парсинг задач происходит каждый час. Если информация о задаче изменилась на сайте, изменения так же касаются и наших данных в БД.
Пример:

![image](https://github.com/Dm-Degtiarev/codeforces_project/assets/123110865/785343b2-5375-4766-a2f7-97c15d22d2c5)

## Используемые технологии:

- Python;
- SQLAlchemy;
- PostgreSQL;
- Pytest;
- Aiogram;


## Запуск проекта

1. #### Клонировать репозиторий, перейти в папку проекта;

2. #### Создать и активировать виртуальное окружение;

3. #### Установить зависимости:

```
pip install -r requirements.txt
```

4.  #### Установить и настроить сервисы:

- PostgreSQL

5.  #### Получить уникальный API Token у https://t.me/BotFather
6.  #### В корне проекта создать файл .env, куда вносим:
 - Реквизиты подключения к БД;
 - Уникальный API Token;
 - Пример заполнения см. в .env.sample.
7.  #### Запустить файл main.py находящийся в корне проекта.

8.  #### Сделать меню быстрых команд у бота (опционально):
![image](https://github.com/Dm-Degtiarev/codeforces_project/assets/123110865/0a47fb06-04f7-45aa-a8ea-b509d48952ec)


## Тестирование

- Для запуска тестов:

```
pytest tests
```
- Для запуска отчета покрытия тестами:
```
coverage report
```
- Для выгрузки html отчета тестирования:
```
coverage html
```
