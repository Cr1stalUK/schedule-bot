import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from itertools import zip_longest
from textwrap import fill
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import CallbackQuery

# Загрузка переменных окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Получение токена бота
API_TOKEN = os.getenv('BOT_TOKEN')

# Проверка наличия токена
if not API_TOKEN:
    logger.error("Не найден BOT_TOKEN в переменных окружения или .env файле")
    raise ValueError("Токен бота не указан. Добавьте BOT_TOKEN в .env файл")

# Инициализация бота
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Далее идет ваш основной код...
# Глобальный словарь для хранения данных пользователей
user_data = {}

# Словарь с группами и их ссылками
groups = {
    "СОД23-1": "http://94.72.18.202:8083/cg59.htm",
    "СОД23-2К": "http://94.72.18.202:8083/cg60.htm",
    "СОД24-1": "http://94.72.18.202:8083/cg61.htm",
    "СОД24-2К": "http://94.72.18.202:8083/cg62.htm",
    "СОД22-1": "http://94.72.18.202:8083/cg63.htm",
    "СОД22-2К": "http://94.72.18.202:8083/cg64.htm",
    "С21-1": "http://94.72.18.202:8083/cg65.htm",
    "С21-2": "http://94.72.18.202:8083/cg66.htm",
    "С21-4К": "http://94.72.18.202:8083/cg67.htm",
    "С21УЗ": "http://94.72.18.202:8083/cg68.htm",
    "С22-1": "http://94.72.18.202:8083/cg69.htm",
    "С22-2": "http://94.72.18.202:8083/cg70.htm",
    "С22-3К": "http://94.72.18.202:8083/cg71.htm",
    "С22уз": "http://94.72.18.202:8083/cg72.htm",
    "С23-1": "http://94.72.18.202:8083/cg73.htm",
    "С23-2": "http://94.72.18.202:8083/cg74.htm",
    "С23-3К": "http://94.72.18.202:8083/cg75.htm",
    "С23УЗ": "http://94.72.18.202:8083/cg76.htm",
    "С24-1": "http://94.72.18.202:8083/cg77.htm",
    "С24-2": "http://94.72.18.202:8083/cg78.htm",
    "С24-3К": "http://94.72.18.202:8083/cg79.htm",
    "С24УЗ": "http://94.72.18.202:8083/cg80.htm",
    "УМД22-1": "http://94.72.18.202:8083/cg81.htm",
    "УМД23-1": "http://94.72.18.202:8083/cg82.htm",
    "УМД24-1": "http://94.72.18.202:8083/cg83.htm",
    "ИМс24-1": "http://94.72.18.202:8083/cg84.htm",
    "СА21-1": "http://94.72.18.202:8083/cg85.htm",
    "СА21-2К": "http://94.72.18.202:8083/cg86.htm",
    "СА22-1": "http://94.72.18.202:8083/cg87.htm",
    "СА22-2": "http://94.72.18.202:8083/cg88.htm",
    "СА23-1": "http://94.72.18.202:8083/cg89.htm",
    "СА23-2": "http://94.72.18.202:8083/cg90.htm",
    "СА24-1": "http://94.72.18.202:8083/cg91.htm",
    "СА24-2": "http://94.72.18.202:8083/cg92.htm",
    "СА24УЗ": "http://94.72.18.202:8083/cg93.htm",
    "ИСа22-1": "http://94.72.18.202:8083/cg94.htm",
    "ИСа23-1": "http://94.72.18.202:8083/cg95.htm",
    "ИСа24-1": "http://94.72.18.202:8083/cg96.htm",
    "ИСп21-1": "http://94.72.18.202:8083/cg97.htm",
    "ИСп21-2К": "http://94.72.18.202:8083/cg98.htm",
    "ИСп22-1": "http://94.72.18.202:8083/cg99.htm",
    "ИСп23-1": "http://94.72.18.202:8083/cg100.htm",
    "ИСп23-2К": "http://94.72.18.202:8083/cg101.htm",
    "ИСп24-1": "http://94.72.18.202:8083/cg102.htm",
    "ИСп24-2К": "http://94.72.18.202:8083/cg103.htm",
    "ИСр22-1": "http://94.72.18.202:8083/cg104.htm",
    "ИСр23-1": "http://94.72.18.202:8083/cg105.htm",
    "ИСр24-1": "http://94.72.18.202:8083/cg106.htm",
    "ИСс22-1": "http://94.72.18.202:8083/cg107.htm",
    "ИСс24-1": "http://94.72.18.202:8083/cg108.htm",
    "СВ22-1К": "http://94.72.18.202:8083/cg109.htm",
    "СВ23-1": "http://94.72.18.202:8083/cg110.htm",
    "СВ23-2К": "http://94.72.18.202:8083/cg111.htm",
    "СВ24-1": "http://94.72.18.202:8083/cg112.htm",
    "СВ24-2К": "http://94.72.18.202:8083/cg113.htm",
    "М22-1": "http://94.72.18.202:8083/cg114.htm",
    "М23-1": "http://94.72.18.202:8083/cg115.htm",
    "М24-1": "http://94.72.18.202:8083/cg116.htm",

}

teachers = {
    "Азарян А.А.": "http://94.72.18.202:8083/cp67.htm",
    "Андрийченко В.А.": "http://94.72.18.202:8083/cp68.htm",
    "Анисимова В.В.": "http://94.72.18.202:8083/cp70.htm",
    "Анищенко Ю.Д.": "http://94.72.18.202:8083/cp133.htm",
    "Анчиков А.И.": "http://94.72.18.202:8083/cp69.htm",
    "Баденкова Ю.А.": "http://94.72.18.202:8083/cp71.htm",
    "Большакова-Стрекалова А.В.": "http://94.72.18.202:8083/cp72.htm",
    "Борисов В.А.": "http://94.72.18.202:8083/cp72.htm",
    "Волошин Р.Н.": "http://94.72.18.202:8083/cp76.htm",
    "Голота Ю.А.": "http://94.72.18.202:8083/cp136.htm",
    "Григорян Н.А.": "http://94.72.18.202:8083/cp77.htm",
    "Гришина С.В.": "http://94.72.18.202:8083/cp78.htm",
    "Дрёмов А.В.": "http://94.72.18.202:8083/cp79.htm",
    "Евстафиева Т.В.": "http://94.72.18.202:8083/cp80.htm",
    "Егорова И.И.": "http://94.72.18.202:8083/cp81.htm",
    "Ефремов И.А.": "http://94.72.18.202:8083/cp82.htm",
    "Журбицкая А.М.": "http://94.72.18.202:8083/cp83.htm",
    "Журский Р.Д.": "http://94.72.18.202:8083/cp84.htm",
    "Иваненко В.А.": "http://94.72.18.202:8083/cp85.htm",
    "Казакова Н.Н.": "http://94.72.18.202:8083/cp86.htm",
    "Каминская Е.В.": "http://94.72.18.202:8083/cp87.htm",
    "Кириченко Д.С.": "http://94.72.18.202:8083/cp135.htm",
    "Кислова Н.В.": "http://94.72.18.202:8083/cp89.htm",
    "Коваль Е.Н.": "http://94.72.18.202:8083/cp90.htm",
    "Колобухова К.В.": "http://94.72.18.202:8083/cp91.htm",
    "Корнева М.И.": "http://94.72.18.202:8083/cp92.htm",
    "Краева М.И.": "http://94.72.18.202:8083/cp93.htm",
    "Куприянова А.П.": "http://94.72.18.202:8083/cp94.htm",
    "Линник О.В.": "http://94.72.18.202:8083/cp96.htm",
    "Лозовицкая М.Ю.": "http://94.72.18.202:8083/cp97.htm",
    "Максимова Н.А.": "http://94.72.18.202:8083/cp99.htm",
    "Малиновская А.Э.": "http://94.72.18.202:8083/cp100.htm",
    "Минбулатова И.Г.": "http://94.72.18.202:8083/cp134.htm",
    "Непочатых А.В.": "http://94.72.18.202:8083/cp102.htm",
    "Омаров А.М.": "http://94.72.18.202:8083/cp137.htm",
    "Передриенко А.С.": "http://94.72.18.202:8083/cp104.htm",
    "Письменчук М.А.": "http://94.72.18.202:8083/cp105.htm",
    "Платунова И.В.": "http://94.72.18.202:8083/cp106.htm",
    "Плешков В.М.": "http://94.72.18.202:8083/cp107.htm",
    "Подгорных О.А": "http://94.72.18.202:8083/cp108.htm",
    "Позднякова Г.А": "http://94.72.18.202:8083/cp109.htm",
    "Разумова А.М": "http://94.72.18.202:8083/cp110.htm",
    "Рыбачек А.А.": "http://94.72.18.202:8083/cp111.htm",
    "Савило С.Ф.": "http://94.72.18.202:8083/cp112.htm",
    "Семёнов А.А.": "http://94.72.18.202:8083/cp114.htm",
    "Спирин В.В.": "http://94.72.18.202:8083/cp115.htm",
    "Сурикова М.И.": "http://94.72.18.202:8083/cp116.htm",
    "Тимофеев Д.М.": "http://94.72.18.202:8083/cp117.htm",
    "Тютюнова Е.В.": "http://94.72.18.202:8083/cp118.htm",
    "Хмеленко В.А.": "http://94.72.18.202:8083/cp120.htm",
    "Хорунжий Д.Г.": "http://94.72.18.202:8083/cp121.htm",
    "Храмов С.С.": "http://94.72.18.202:8083/cp122.htm",
    "Чертищев В.А.": "http://94.72.18.202:8083/cp123.htm",
    "Шадрина О.А.": "http://94.72.18.202:8083/cp124.htm",
    "Шаройкина Т.Я.": "http://94.72.18.202:8083/cp126.htm",
    "Шевченко П.С.": "http://94.72.18.202:8083/cp127.htm",
    "Шипицина М.А.": "http://94.72.18.202:8083/cp128.htm",
    "Юнкевич П.С.": "http://94.72.18.202:8083/cp129.htm",
    "Юрченко Е.В.": "http://94.72.18.202:8083/cp130.htm",
    "Яковенко П.В.": "http://94.72.18.202:8083/cp132.htm",
    
}

default_times = {
    "1": "8:30-10:00",
    "2": "10:10-11:40",
    "3": "12:10-13:40",
    "4": "13:50-15:20",
    "5": "15:30-17:00",
    "6": "17:10-18:40"
}

monday_times = {
    "1": "8:30-9:00",
    "2": "9:10-10:30",
    "3": "10:40-12:00",
    "4": "12:20-13:40",
    "5": "13:50-15:10",
    "6": "16:00-17:20",
    "7": "17:30-18:50"
}
# Кэш для хранения расписания
schedule_cache = {}

def get_weekday_name(offset=0):
    """Возвращает 'пн', 'вт' и т.д. с учётом смещения дней"""
    days = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
    today = datetime.now() + timedelta(days=offset)
    return days[today.weekday()]

def split_schedule(schedule_text, max_length=4096):
    """
    Разбивает текст расписания на части, каждая из которых не превышает max_length символов.
    """
    parts = []
    while len(schedule_text) > max_length:
        # Находим последний перенос строки до max_length
        split_index = schedule_text.rfind('\n', 0, max_length)
        if split_index == -1:
            # Если перенос строки не найден, просто делим по max_length
            split_index = max_length
        parts.append(schedule_text[:split_index])
        schedule_text = schedule_text[split_index:].lstrip()
    parts.append(schedule_text)
    return parts

async def get_schedule(group_url):
    # Проверяем, есть ли данные в кэше и не устарели ли они
    if group_url in schedule_cache:
        cached_data = schedule_cache[group_url]
        if datetime.now() - cached_data['timestamp'] < timedelta(minutes=5):
            logger.info(f"Используем кэшированное расписание для {group_url}")
            return cached_data['schedule']

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(group_url) as response:
                if response.status == 200:
                    html = await response.text(encoding='windows-1251')
                    soup = BeautifulSoup(html, 'html.parser')

                    tables = soup.find_all('table')
                    if not tables:
                        logger.warning("Таблицы на странице не найдены.")
                        return []

                    schedule = []
                    current_date = None

                    for table in tables:
                        rows = table.find_all('tr')
                        for row in rows[1:]:  # Пропускаем заголовок
                            cells = row.find_all('td')

                            if not cells:
                                continue

                            # Проверяем, является ли строка заголовком
                            is_header = any(
                                cell.text.strip() in ["День", "Пара", "&nbsp;"]
                                for cell in cells
                            )
                            if is_header:
                                continue  # Пропускаем заголовок

                            # Если строка содержит дату и день недели
                            if len(cells) >= 1 and cells[0].get('rowspan'):
                                current_date = cells[0].text.strip().replace('\n', ' ')
                                logger.info(f"Найдена дата: {current_date}")

                            # Определяем номер пары и ячейку с деталями
                            pair_number = None
                            details_cell = None
                            
                            if len(cells) >= 3:  # Строка с датой
                                pair_number = cells[1].text.strip()
                                details_cell = cells[2]
                            elif len(cells) >= 2:  # Обычная строка
                                pair_number = cells[0].text.strip()
                                details_cell = cells[1]
                            
                            if not pair_number or not details_cell or not details_cell.text.strip():
                                continue

                            # Извлекаем данные о паре
                            subject = details_cell.find('a', class_='z1')
                            classroom = details_cell.find('a', class_='z2')
                            teacher = details_cell.find('a', class_='z3')

                            # Определяем время пары
                            is_monday = current_date and ("Пн" in current_date or "понедельник" in current_date.lower())
                            time_table = monday_times if is_monday else default_times
                            pair_time = time_table.get(pair_number, "—")

                            schedule.append({
                                'date': current_date,
                                'pair_number': pair_number,
                                'pair_time': pair_time,
                                'subject': subject.text.strip() if subject else "Нет пары",
                                'classroom': classroom.text.strip() if classroom else "—",
                                'teacher': teacher.text.strip() if teacher else "—"
                            })

                    # Сохраняем расписание в кэше
                    schedule_cache[group_url] = {
                        'schedule': schedule,
                        'timestamp': datetime.now()
                    }

                    logger.info(f"Расписание успешно загружено для {group_url}")
                    return schedule
                else:
                    logger.error(f"Ошибка при загрузке страницы: {response.status}")
                    return []
    except Exception as e:
        logger.error(f"Ошибка в функции get_schedule: {e}")
        return []

@dp.message(Command("remove"))
async def remove_keyboard(message: Message):
    await message.answer(
        "Старая клавиатура удалена",
        reply_markup=ReplyKeyboardRemove()
    )

# Команда /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    logger.info(f"Пользователь {message.from_user.id} запустил бота.")
    
    # Создаем клавиатуру с тремя кнопками
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🆘 Помощь", callback_data="help_command")],
        [InlineKeyboardButton(text="📅 Выберите день", callback_data="select_day")],
        [InlineKeyboardButton(text="🏫 Список групп", callback_data="groups_list")],
        [InlineKeyboardButton(text="👨‍🏫 Список преподавателей", callback_data="teachers_list")]
    ])
    
    await message.reply(
        "Привет! Я бот для расписания. Выбери действие:",
        reply_markup=keyboard
    )

# Команда /schedule
@dp.message(Command("schedule"))
async def send_schedule(message: Message):
    try:
        # Получаем название группы из сообщения
        group_name = message.text.split()[1]
        logger.info(f"Пользователь {message.from_user.id} запросил расписание для группы {group_name}.")

        # Ищем группу в словаре
        if group_name in groups:
            group_url = groups[group_name]
            schedule = await get_schedule(group_url)

            if schedule:
                response = f"📅 Расписание для группы {group_name}:\n"
                current_date = None

                for entry in schedule:
                    if entry['date'] != current_date:
                        response += f"\n📅 <b>{entry['date']}</b>\n"
                        current_date = entry['date']
                    response += f"  🕒 Пара {entry['pair_number']} ({entry['pair_time']}):\n"
                    response += f"      📚 Дисциплина: {entry['subject']}\n"
                    response += f"      🏫 Аудитория: {entry['classroom']}\n"
                    response += f"      👨‍🏫 Преподаватель: {entry['teacher']}\n\n"

                # Разбиваем расписание на части
                schedule_parts = split_schedule(response)

                # Отправляем каждую часть отдельным сообщением
                for part in schedule_parts:
                    await message.reply(part)

                logger.info(f"Расписание отправлено пользователю {message.from_user.id}.")
            else:
                await message.reply("Не удалось загрузить расписание.")
                logger.warning(f"Не удалось загрузить расписание для группы {group_name}.")
        else:
            await message.reply("Группа не найдена. Проверь название группы.")
            logger.warning(f"Группа {group_name} не найдена в словаре.")
    except IndexError:
        await message.reply("Используй команду так: /schedule <группа>")
        logger.warning("Пользователь ввел команду /schedule без указания группы.")
    except Exception as e:
        await message.reply("Произошла ошибка при обработке запроса.")
        logger.error(f"Ошибка в команде /schedule: {e}")

# Команда /teacher
@dp.message(Command("teacher"))
async def send_teacher_schedule(message: Message):
    try:
        # Получаем имя преподавателя из сообщения
        teacher_name = " ".join(message.text.split()[1:])
        logger.info(f"Пользователь {message.from_user.id} запросил расписание для преподавателя {teacher_name}.")

        # Ищем преподавателя в словаре
        if teacher_name in teachers:
            teacher_url = teachers[teacher_name]
            schedule = await get_schedule(teacher_url)

            if schedule:
                response = f"📅 Расписание для преподавателя {teacher_name}:\n"
                current_date = None

                for entry in schedule:
                    if entry['date'] != current_date:
                        response += f"\n📅 <b>{entry['date']}</b>\n"
                        current_date = entry['date']
                    response += f"  🕒 Пара {entry['pair_number']} ({entry['pair_time']})\n"
                    response += f"      📚 Дисциплина: {entry['teacher']}\n"
                    response += f"      👥 Группа: {entry['subject']}\n"
                    response += f"      🏫 Аудитория: {entry['classroom']}\n\n"

                # Разбиваем расписание на части
                schedule_parts = split_schedule(response)

                # Отправляем каждую часть отдельным сообщением
                for part in schedule_parts:
                    await message.reply(part)

                logger.info(f"Расписание отправлено пользователю {message.from_user.id}.")
            else:
                await message.reply("Не удалось загрузить расписание.")
                logger.warning(f"Не удалось загрузить расписание для преподавателя {teacher_name}.")
        else:
            await message.reply("Преподаватель не найден. Проверь имя преподавателя.")
            logger.warning(f"Преподаватель {teacher_name} не найден в словаре.")
    except IndexError:
        await message.reply("Используй команду так: /teacher <имя преподавателя>")
        logger.warning("Пользователь ввел команду /teacher без указания имени преподавателя.")
    except Exception as e:
        await message.reply("Произошла ошибка при обработке запроса.")
        logger.error(f"Ошибка в команде /teacher: {e}")

# Остальные функции (help, teachers, groups) остаются без изменений

# Команда /help
@dp.message(Command("help"))
async def send_help(message: Message):
    logger.info(f"Пользователь {message.from_user.id} запросил помощь.")
    help_text = (
        "📚 <b>Доступные команды:</b>\n\n"
        "🔹 /start - Начать работу с ботом\n"
        "🔹 /help - Показать это сообщение\n\n"
        "📅 <b>Расписание:</b>\n"
        "🔹 /schedule [группа] - Расписание группы на неделю\n"
        "🔹 /teacher [ФИО] - Расписание преподавателя\n"
        "🔹 /day [группа/ФИО] [день] - Расписание на конкретный день\n\n"
        "📋 <b>Списки:</b>\n"
        "🔹 /groups - Все доступные группы\n"
        "🔹 /teachers - Все преподаватели\n\n"
        "📌 <b>Примеры:</b>\n"
        "<code>/schedule СОД23-1</code>\n"
        "<code>/teacher Волошин Р.Н.</code>\n"
        "<code>/day ИСп21-2К пн</code>\n"
        "<code>/day Григорян Н.А. среда</code>"
    )
    await message.reply(help_text, parse_mode=ParseMode.HTML)

# Команда /groups
@dp.message(Command("groups"))
async def send_groups(message: Message):
    logger.info(f"Пользователь {message.from_user.id} запросил список групп.")
    
    # Создаем клавиатуру с кнопками
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    # Группируем кнопки по 3 в ряд
    group_buttons = []
    for group in sorted(groups.keys()):
        group_buttons.append(InlineKeyboardButton(text=group, callback_data=f"group_{group}"))
        if len(group_buttons) == 3:
            keyboard.inline_keyboard.append(group_buttons)
            group_buttons = []
    
    # Добавляем оставшиеся кнопки
    if group_buttons:
        keyboard.inline_keyboard.append(group_buttons)
    
    await message.reply("🏫 Выберите группу:", reply_markup=keyboard)

# Команда /teachers
@dp.message(Command("teachers"))
async def send_teachers(message: Message):
    logger.info(f"Пользователь {message.from_user.id} запросил список преподавателей.")
    
    # Создаем клавиатуру с кнопками
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    # Группируем кнопки по 2 в ряд (так как ФИО длинные)
    teacher_buttons = []
    for teacher in sorted(teachers.keys()):
        teacher_buttons.append(InlineKeyboardButton(text=teacher, callback_data=f"teacher_{teacher}"))
        if len(teacher_buttons) == 2:
            keyboard.inline_keyboard.append(teacher_buttons)
            teacher_buttons = []
    
    # Добавляем оставшиеся кнопки
    if teacher_buttons:
        keyboard.inline_keyboard.append(teacher_buttons)
    
    await message.reply("👨‍🏫 Выберите преподавателя:", reply_markup=keyboard)

# Глобальный словарь для хранения состояния (временное решение)
user_state = {}

# Глобальный словарь для хранения состояния
# Глобальный словарь для хранения состояния
user_state = {}

@dp.callback_query(lambda c: c.data == "select_day")
async def select_day(callback: CallbackQuery):
    try:
        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        for i in range(0, len(days), 2):
            row = days[i:i+2]
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(text=day, callback_data=f"day_{day.lower()}") 
                for day in row
            ])
        
        await callback.message.edit_text("📅 Выберите день недели:", reply_markup=keyboard)
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка в select_day: {e}")
        await callback.answer("Произошла ошибка. Попробуйте снова.")

@dp.callback_query(lambda c: c.data.startswith("day_") and len(c.data.split("_")) == 2)
async def day_selected(callback: CallbackQuery):
    try:
        day = callback.data.split("_")[1]
        user_state[callback.from_user.id] = {"day": day}
        logger.info(f"Пользователь {callback.from_user.id} выбрал день: {day}")
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏫 Группы", callback_data=f"day_category_groups")],
            [InlineKeyboardButton(text="👨‍🏫 Преподаватели", callback_data=f"day_category_teachers")]
        ])
        
        await callback.message.edit_text(
            f"Выбран день: {day.capitalize()}. Теперь выберите категорию:",
            reply_markup=keyboard
        )
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка в day_selected: {e}")
        await callback.answer("Произошла ошибка. Попробуйте снова.")

@dp.callback_query(lambda c: c.data.startswith("day_category_"))
async def show_category_options(callback: CallbackQuery):
    try:
        parts = callback.data.split("_")
        if len(parts) < 3:
            await callback.answer("❌ Неверный формат данных", show_alert=True)
            return
            
        category = parts[2]  # groups или teachers
        day = user_state.get(callback.from_user.id, {}).get("day", "")
        
        if not day:
            await callback.answer("❌ День не выбран", show_alert=True)
            return
        
        if category == "groups":
            items = sorted(groups.keys())
            text = "🏫 Выберите группу:"
            prefix = "group"
            
            # Обработка для групп (удаляем только дефисы)
            def process_item(item):
                return item.replace("-", "")
                
        else:
            items = sorted(teachers.keys())
            text = "👨‍🏫 Выберите преподавателя:"
            prefix = "teacher"
            
            # Обработка для преподавателей (создаем уникальный ключ)
            def process_item(item):
                # Используем хэш для длинных имен
                return str(hash(item))[:16]
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        
        # Словарь для хранения соответствий
        name_mapping = {}
        
        for i in range(0, len(items), 2):
            row = items[i:i+2]
            buttons = []
            for item in row:
                safe_key = process_item(item)
                name_mapping[safe_key] = item  # Сохраняем соответствие
                callback_data = f"day_final_{prefix}_{day}_{safe_key}"
                
                # Проверяем длину callback_data
                if len(callback_data.encode('utf-8')) > 64:
                    callback_data = f"day_{prefix}_{day[:3]}_{safe_key[:8]}"
                
                buttons.append(InlineKeyboardButton(
                    text=item, 
                    callback_data=callback_data
                ))
            keyboard.inline_keyboard.append(buttons)
        
        # Сохраняем mapping в user_state
        user_state[callback.from_user.id]["name_mapping"] = name_mapping
        
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка в show_category_options: {str(e)}", exc_info=True)
        await callback.answer("❌ Произошла ошибка", show_alert=True)

@dp.callback_query(lambda c: c.data.startswith("day_final_"))
async def show_final_schedule(callback: CallbackQuery):
    try:
        # Получаем данные из callback
        parts = callback.data.split('_')
        if len(parts) < 4:
            await callback.answer("❌ Неверный формат данных", show_alert=True)
            return
            
        entity_type = parts[2]  # 'group' или 'teacher'
        day = parts[3]
        safe_key = '_'.join(parts[4:])
        
        # Получаем сохраненные соответствия имен
        name_mapping = user_state.get(callback.from_user.id, {}).get("name_mapping", {})
        
        # Восстанавливаем оригинальное имя
        if entity_type == 'teacher':
            # Для преподавателей используем сохраненное соответствие
            original_name = name_mapping.get(safe_key)
            if not original_name:
                # Альтернативный поиск для совместимости
                original_name = next(
                    (k for k in teachers.keys() 
                     if k.replace(".", "").replace("-", "").replace(" ", "_").lower() == safe_key.lower()),
                    None
                )
            
            if not original_name:
                logger.error(f"Преподаватель не найден: {safe_key}")
                await callback.answer("❌ Преподаватель не найден", show_alert=True)
                return
                
            url = teachers[original_name]
        else:
            # Для групп используем прямое соответствие (без дефисов)
            original_name = next(
                (k for k in groups.keys() 
                 if k.replace("-", "").lower() == safe_key.lower()),
                None
            )
            if not original_name:
                await callback.answer("❌ Группа не найдена", show_alert=True)
                return
            url = groups[original_name]
        
        logger.info(f"Загружаем расписание для {original_name}")

        # Получаем расписание
        schedule = await get_schedule(url)
        if not schedule:
            logger.error("Не удалось загрузить расписание")
            await callback.answer("❌ Расписание недоступно", show_alert=True)
            return
        
        # Фильтруем по выбранному дню
        day_variants = {
            'понедельник': ['пн', 'понедельник'],
            'вторник': ['вт', 'вторник'],
            'среда': ['ср', 'среда'],
            'четверг': ['чт', 'четверг'],
            'пятница': ['пт', 'пятница'],
            'суббота': ['сб', 'суббота']
        }.get(day, [])
        
        filtered = []
        for entry in schedule:
            if not entry.get('date'):
                continue
                
            entry_day = entry['date'].lower()
            if any(variant in entry_day for variant in day_variants):
                filtered.append(entry)
        
        # Формируем ответ
        if not filtered:
            response = f"📅 У {original_name} нет пар в {day.capitalize()}"
        else:
            response = f"📅 Расписание {original_name} на {day.capitalize()}:\n\n"
            for entry in filtered:
                response += f"  🕒 Пара {entry.get('pair_number', '?')} ({entry.get('pair_time', '')})\n"
                if entity_type == 'group':
                    response += f"      📚 Дисциплина: {entry.get('subject', 'Не указано')}\n"
                    response += f"      🏫 Аудитория: {entry.get('classroom', 'Не указано')}\n"
                    response += f"      👨‍🏫 Преподаватель: {entry.get('teacher', 'Не указано')}\n\n"
                else:
                    response += f"      📚 Дисциплина: {entry.get('teacher', 'Не указано')}\n"
                    response += f"      👥 Группа: {entry.get('subject', 'Не указано')}\n"
                    response += f"      🏫 Аудитория: {entry.get('classroom', 'Не указано')}\n\n"
        
        # Отправляем результат
        await callback.message.edit_text(response, reply_markup=None)
        await callback.answer()
        
    except Exception as e:
        logger.error(f"Ошибка в show_final_schedule: {str(e)}", exc_info=True)
        await callback.answer("❌ Произошла ошибка", show_alert=True)

# Обработчик нажатий на кнопки
@dp.callback_query()
async def process_callback(callback: types.CallbackQuery):
    try:
        data = callback.data
        
        if data == "help_command":
            help_text = (
                "📚 <b>Доступные команды:</b>\n\n"
                "🔹 /start - Начать работу с ботом\n"
                "🔹 /help - Показать это сообщение\n\n"
                "📅 <b>Расписание:</b>\n"
                "🔹 /schedule [группа] - Расписание группы на неделю\n"
                "🔹 /teacher [ФИО] - Расписание преподавателя\n"
                "🔹 /day [группа/ФИО] [день] - Расписание на конкретный день\n\n"
                "📋 <b>Списки:</b>\n"
                "🔹 /groups - Все доступные группы\n"
                "🔹 /teachers - Все преподаватели\n\n"
                "📌 <b>Примеры:</b>\n"
                "<code>/schedule СОД23-1</code>\n"
                "<code>/teacher Волошин Р.Н.</code>\n"
                "<code>/day ИСп21-2К пн</code>\n"
                "<code>/day Григорян Н.А. среда</code>"
            )
            
            # Проверяем, отличается ли новое сообщение от текущего
            current_text = callback.message.text or callback.message.caption or ""
            if (current_text.strip() != help_text.strip() or 
                callback.message.reply_markup is not None):
                await callback.message.edit_text(
                    help_text, 
                    parse_mode=ParseMode.HTML,
                    reply_markup=None
                )
            else:
                await callback.answer("Вы уже просматриваете справку")
            
        elif data == "groups_list":
            # Проверяем, не открыт ли уже список групп
            if "Выберите группу" not in (callback.message.text or ""):
                keyboard = InlineKeyboardMarkup(inline_keyboard=[])
                group_buttons = []
                for group in sorted(groups.keys()):
                    group_buttons.append(InlineKeyboardButton(text=group, callback_data=f"group_{group}"))
                    if len(group_buttons) == 3:
                        keyboard.inline_keyboard.append(group_buttons)
                        group_buttons = []
                
                if group_buttons:
                    keyboard.inline_keyboard.append(group_buttons)
                
                await callback.message.edit_text("🏫 Выберите группу:", reply_markup=keyboard)
            else:
                await callback.answer("Список групп уже открыт")
        
        elif data == "teachers_list":
            # Проверяем, не открыт ли уже список преподавателей
            if "Выберите преподавателя" not in (callback.message.text or ""):
                keyboard = InlineKeyboardMarkup(inline_keyboard=[])
                teacher_buttons = []
                for teacher in sorted(teachers.keys()):
                    teacher_buttons.append(InlineKeyboardButton(text=teacher, callback_data=f"teacher_{teacher}"))
                    if len(teacher_buttons) == 2:
                        keyboard.inline_keyboard.append(teacher_buttons)
                        teacher_buttons = []
                
                if teacher_buttons:
                    keyboard.inline_keyboard.append(teacher_buttons)
                
                await callback.message.edit_text("👨‍🏫 Выберите преподавателя:", reply_markup=keyboard)
            else:
                await callback.answer("Список преподавателей уже открыт")
        
        elif data.startswith("group_"):
            group_name = data[6:]
            if group_name in groups:
                group_url = groups[group_name]
                schedule = await get_schedule(group_url)
                
                if schedule:
                    response = f"📅 Расписание для группы {group_name}:\n"
                    current_date = None

                    for entry in schedule:
                        if entry['date'] != current_date:
                            response += f"\n📅 <b>{entry['date']}</b>\n"
                            current_date = entry['date']
                        response += f"  🕒 Пара {entry['pair_number']} ({entry['pair_time']})\n"
                        response += f"      📚 Дисциплина: {entry['subject']}\n"
                        response += f"      🏫 Аудитория: {entry['classroom']}\n"
                        response += f"      👨‍🏫 Преподаватель: {entry['teacher']}\n\n"

                    schedule_parts = split_schedule(response)
                    await callback.message.edit_reply_markup(reply_markup=None)
                    await callback.message.answer(schedule_parts[0])

                    for part in schedule_parts[1:]:
                        await callback.message.answer(part)
                else:
                    await callback.answer("Не удалось загрузить расписание.", show_alert=True)
            else:
                await callback.answer("Группа не найдена.", show_alert=True)
        
        elif data.startswith("teacher_"):
            teacher_name = data[8:]
            if teacher_name in teachers:
                teacher_url = teachers[teacher_name]
                schedule = await get_schedule(teacher_url)
                
                if schedule:
                    response = f"📅 Расписание для преподавателя {teacher_name}:\n"
                    current_date = None

                    for entry in schedule:
                        if entry['date'] != current_date:
                            response += f"\n📅 <b>{entry['date']}</b>\n"
                            current_date = entry['date']
                        response += f"  🕒 Пара {entry['pair_number']} ({entry['pair_time']})\n"
                        response += f"      📚 Дисциплина: {entry['teacher']}\n"
                        response += f"      👥 Группа: {entry['subject']}\n"
                        response += f"      🏫 Аудитория: {entry['classroom']}\n\n"

                    schedule_parts = split_schedule(response)
                    await callback.message.edit_reply_markup(reply_markup=None)
                    await callback.message.answer(schedule_parts[0])

                    for part in schedule_parts[1:]:
                        await callback.message.answer(part)
                else:
                    await callback.answer("Не удалось загрузить расписание.", show_alert=True)
            else:
                await callback.answer("Преподаватель не найден.", show_alert=True)
        
        await callback.answer()
    
    except Exception as e:
        logger.error(f"Ошибка в обработчике callback: {e}")
        await callback.answer("Произошла ошибка. Попробуйте снова.", show_alert=True)


# Добавим в существующий код (после других команд)

@dp.message(Command("day"))
async def day_schedule(message: Message):
    try:
        args = message.text.split()
        if len(args) < 3:
            await message.reply("❌ Недостаточно аргументов. Формат: /day <группа/преподаватель> <день>")
            return

        target = " ".join(args[1:-1])  # Для ФИО с пробелами
        day_name = args[-1].lower()

        weekdays = {
            "пн": ["пн", "понедельник"],
            "вт": ["вт", "вторник"],
            "ср": ["ср", "среда"],
            "чт": ["чт", "четверг"],
            "пт": ["пт", "пятница"],
            "сб": ["сб", "суббота"],
            "вс": ["вс", "воскресенье"]
        }

        # Проверяем день
        day_found = None
        for day_key, day_variants in weekdays.items():
            if day_name in day_variants:
                day_found = day_key
                break

        if not day_found:
            await message.reply("❌ Неверный день недели. Используйте: пн, вт, ср, чт, пт, сб, вс")
            return

        # Ищем цель (группу или преподавателя)
        url = None
        response_title = ""
        if target in groups:
            url = groups[target]
            response_title = f"📅 Расписание группы {target} на {day_name}:\n"
        elif target in teachers:
            url = teachers[target]
            response_title = f"📅 Расписание преподавателя {target} на {day_name}:\n"
        else:
            await message.reply("❌ Группа или преподаватель не найдены")
            return

        schedule = await get_schedule(url)
        logger.info(f"Загружено расписание: {len(schedule)} записей")  # Логируем

        if not schedule:
            await message.reply("⚠️ Не удалось загрузить расписание")
            return

        # Фильтруем по дню
        filtered = []
        for entry in schedule:
            entry_day = entry['date'].lower()
            if any(day in entry_day for day in weekdays[day_found]):
                filtered.append(entry)

        if not filtered:
            await message.reply(f"ℹ️ Пар в {day_name} нет")
            return

        # Формируем ответ
        response = response_title
        current_date = None

        for entry in filtered:
            if entry['date'] != current_date:
                response += f"\n📅 <b>{entry['date']}</b>\n"
                current_date = entry['date']

            response += f"  🕒 Пара {entry['pair_number']} ({entry['pair_time']})\n"
    
            if target in groups:
                response += f"      📚 Дисциплина: {entry['subject']}\n"
                response += f"      🏫 Аудитория: {entry['classroom']}\n"
                response += f"      👨‍🏫 Преподаватель: {entry['teacher']}\n\n"
            else:
                response += f"      📚 Дисциплина: {entry['teacher']}\n"
                response += f"      👥 Группа: {entry['subject']}\n"
                response += f"      🏫 Аудитория: {entry['classroom']}\n\n"

        await message.reply(response)

    except Exception as e:
        logger.error(f"Ошибка в /day: {str(e)}", exc_info=True)
        await message.reply("⚠️ Произошла ошибка. Попробуйте позже")

# Обработка неизвестных команд
@dp.message()
async def handle_unknown_command(message: Message):
    await message.reply("Неизвестная команда. Используй /help для списка команд.")

# Запуск бота
async def main():
    logger.info("Бот запущен.")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())