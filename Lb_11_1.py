import psycopg2
import csv

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="12345",  
    host="localhost",
    port="5432"
)
cur = conn.cursor()

def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook_2 (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100),
            phone VARCHAR(20)
        )
    """)
    conn.commit()

# Функция для поиска по шаблону
def search_phonebook(pattern):
    cur.execute("""
        SELECT id, username, phone
        FROM phonebook_2
        WHERE username ILIKE %s OR phone LIKE %s
    """, (f"%{pattern}%", f"%{pattern}%"))
    return cur.fetchall()

# Процедура для вставки или обновления пользователя
def insert_or_update_user(username, phone):
    cur.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM phonebook_2 WHERE username = %s) THEN
                UPDATE phonebook_2
                SET phone = %s
                WHERE username = %s;
            ELSE
                INSERT INTO phonebook_2 (username, phone)
                VALUES (%s, %s);
            END IF;
        END;
        $$;
    """, (username, phone, username, username, phone))
    conn.commit()

# Процедура для вставки нескольких пользователей
def insert_multiple_users(user_list):
    invalid_data = []
    for user_data in user_list:
        name, phone = user_data.split(',')
        if len(phone) != 10:  
            invalid_data.append(user_data)
        else:
            insert_or_update_user(name, phone)
    
    if invalid_data:
        print(f"Некорректные данные: {invalid_data}")
    else:
        print("Все данные успешно добавлены.")

# Функция для пагинации
def get_paginated_phonebook(limit_val, offset_val):
    cur.execute("""
        SELECT id, username, phone
        FROM phonebook_2
        ORDER BY username
        LIMIT %s OFFSET %s
    """, (limit_val, offset_val))
    return cur.fetchall()

# Процедура для удаления пользователя по имени или телефону
def delete_user_by_username_or_phone(input_value):
    cur.execute("""
        DELETE FROM phonebook_2 WHERE username = %s;
    """, (input_value,))
    if cur.rowcount == 0:
        cur.execute("""
            DELETE FROM phonebook_2 WHERE phone = %s;
        """, (input_value,))
    conn.commit()

# Вставка данных из CSV
def insert_from_csv():
    with open('contacs.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            insert_or_update_user(row['username'], row['phone'])
    print("Данные из CSV успешно добавлены")

# Вставка вручную
def insert_from_input():
    username = input("Введите имя: ")
    phone = input("Введите номер: ")
    insert_or_update_user(username, phone)
    print("Добавлено")

# Обновление данных
def update_data():
    username = input("Введите имя пользователя, которого хотите обновить: ")
    new_phone = input("Введите новый номер: ")
    insert_or_update_user(username, new_phone)
    print("Обновлено успешно")

# Поиск
def search_data():
    pattern = input("Введите часть имени или номера для поиска: ")
    results = search_phonebook(pattern)
    if results:
        for row in results:
            print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")
    else:
        print("Нет результатов")

# Удаление
def delete_data():
    choice = input("Удалить по (1 - имени, 2 - номеру): ")
    if choice == '1':
        name = input("Введите имя: ")
        delete_user_by_username_or_phone(name)
    else:
        phone = input("Введите номер: ")
        delete_user_by_username_or_phone(phone)
    print("Данные удалены")

# Показать все контакты
def show_all():
    cur.execute("SELECT * FROM phonebook_2")
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")
    else:
        print("Нет данных")

# Главное меню
def menu():
    create_table()
    while True:
        print("\nТелефонная книга")
        print("1. Вставка из CSV")
        print("2. Вставка вручную")
        print("3. Обновить номер")
        print("4. Поиск")
        print("5. Удаление")
        print("6. Вывод всех контактов")
        print("0. Выход")

        choice = input("Выбор: ")
        if choice == '1':
            insert_from_csv()
        elif choice == '2':
            insert_from_input()
        elif choice == '3':
            update_data()
        elif choice == '4':
            search_data()
        elif choice == '5':
            delete_data()
        elif choice == '6':
            show_all()
        elif choice == '0':
            break
        else:
            print("От 0 до 6...")

    cur.close()
    conn.close()

if __name__ == "__main__":
    menu()
