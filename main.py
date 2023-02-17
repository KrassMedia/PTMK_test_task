from sys import argv
from datetime import datetime
from time import time

from random import randint, choice
import sqlite3

from dateutil.relativedelta import relativedelta

ListNames = [
	['Рогов', 'Мухин', 'Исаев', 'Курский', 'Бойков', 'Попов', 'Сидоров', 'Петров', 'Федоров', 'Федотов'],
	['Андрей', 'Иван', 'Владимир', 'Василий', 'Николай', 'Альберт', 'Федот', 'Федор', 'Александр'],
	['Петрович', 'Адреевич', 'Иванов', 'Владимирович', 'Васильевич', 'Николаевич', 'Геннадьевич', 'Александрович'],
	['Рогова', 'Мухина', 'Исаева', 'Курская', 'Бойкова', 'Попова', 'Сидорова', 'Петрова', 'Федорова', 'Федотова'],
	['Екатерина', 'Федора', 'Яна', 'Мария', 'Марина', 'Анастасия', 'Надежда', 'Юлия', 'Кристина', 'Фрося', 'Виктория'],
	['Петровна', 'Андреевна', 'Ивановна', 'Владимировна', 'Васильевна', 'Николаевна', 'Геннадьевна', 'Александровна']
]


def create_table(db):
	cursor = db.cursor()
	query = 'CREATE TABLE peoples (' \
		'id INTEGER PRIMARY KEY, ' \
		'full_name TEXT NOT NULL, ' \
		'birth_day TEXT NOT NULL,' \
		'gender INTEGER NOT NULL);'
	try:
		cursor.execute(query)
		db.commit()
		print('Таблица успешно создана!')
	except sqlite3.Error as error:
		print("Ошибка при создании таблицы:", error)
	cursor.close()


def add_write(db, full_name, birth_day, gender):
	res = True
	cursor = db.cursor()
	query = "INSERT INTO peoples (id, full_name, birth_day, gender) " \
		f"VALUES  (null, '{full_name}', '{birth_day}', {gender});"
	try:
		cursor.execute(query)
		db.commit()
	except sqlite3.Error as error:
		print("Ошибка при добавлении записи в таблицу:", error)
		res = False
	cursor.close()
	return res


def print_data(db, filter_mark=False):
	cursor = db.cursor()
	if not filter_mark:
		query = "SELECT DISTINCT (full_name || ' ' || birth_day), full_name, birth_day,  gender " \
				"FROM peoples ORDER BY full_name;"
	else:
		query = "SELECT * FROM peoples WHERE gender = 1 AND full_name LIKE 'Ф%';"

	records = None
	load_time = 0
	try:
		load_time = time()
		cursor.execute(query)
		load_time = time() - load_time
		records = cursor.fetchall()
	except sqlite3.Error as error:
		print("Ошибка при запросе данных из таблицы:", error)

	if filter_mark:
		print('Время выполнения SQL запроса:', round(load_time, 3), 'сек.')
	else:
		if records:
			for line in records:
				full_year = relativedelta(datetime.now(), datetime.strptime(line[2], '%Y-%m-%d')).years
				print(line[1], line[2], 'Муж.' if line[3] else 'Жен.', full_year)

	cursor.close()


def get_rand_person():
	gender = randint(0, 1)
	fio = f'{choice(ListNames[0])} {choice(ListNames[1])} {choice(ListNames[2])}' if gender else \
		f'{choice(ListNames[3])} {choice(ListNames[4])} {choice(ListNames[5])}'
	birth_day = datetime(randint(1930, 2022), randint(1, 12), randint(1, 28)).date()
	return fio, birth_day, gender


def main():
	if len(argv) < 2:
		return

	db = sqlite3.connect('database.db')

	match argv[1]:
		case '1':
			create_table(db)
		case '2':
			if len(argv) == 7:
				try:
					full_name = f'{argv[2]} {argv[3]} {argv[4]}'
					birth_day = datetime.strptime(argv[5], '%d.%m.%Y').date()
					gender = 0 if argv[6].startswith('Ж') or argv[6].startswith('F') else 1
					if add_write(db, full_name, birth_day, gender):
						print('Запись успешно добавлена в таблицу!')
				except ValueError:
					print('Введен не верный формат данных! Пример: Фамилия Имя Отчество 03.09.1991 М')
			else:
				print('Введен не верный формат данных! Пример: Фамилия Имя Отчество 03.09.1991 М')
		case '3':
			print_data(db)
		case '4':
			for _ in range(1000000):
				if not add_write(db, *get_rand_person()):
					break
			print('Рандомное заполнение таблицы завершено!')
		case '5':
			print_data(db, True)

	db.close()


if __name__ == '__main__':
	main()
