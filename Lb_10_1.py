import psycopg2
import csv

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="12345",  
    host="localhost",
    port="5432"

)
cur = conn.cursor()

# Создание таблицы
def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100),
            phone VARCHAR(20)
        )
    """)
    conn.commit()

# Вставка данных из CSV
def insert_from_csv():
    with open('contacs.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (row['username'], row['phone']))
            conn.commit()
    print("Данные из CSV успешно добавлены")


# Вставка вручную
def insert_from_input():
    username = input("Введите имя: ")
    phone = input("Введите номер: ")
    cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (username, phone))
    conn.commit()
    print("Добавлено")

# Обновление данных
def update_data():
    username = input("Введите имя пользователя, которого хотите обновить: ")
    new_phone = input("Введите новый номер: ")
    cur.execute("UPDATE phonebook SET phone = %s WHERE username = %s", (new_phone, username))
    conn.commit()
    print("Обновлено успешно")

# Поиск
def search_data():
    filter_type = input("Фильтр по (1 - имени, 2 - номеру): ")
    if filter_type == '1':
        name = input("Введите имя: ")
        cur.execute("SELECT * FROM phonebook WHERE username LIKE %s", (f"%{name}%",))
    else:
        phone = input("Введите номер: ")
        cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
    results = cur.fetchall()
    for row in results:
        print(row)

# Удаление
def delete_data():
    choice = input("Удалить по (1 - имени, 2 - номеру): ")
    if choice == '1':
        name = input("Введите имя: ")
        cur.execute("DELETE FROM phonebook WHERE username = %s", (name,))
    else:
        phone = input("Введите номер: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    conn.commit()
    print("Данные удалены")

def show_all():
    cur.execute("SELECT * FROM phonebook")
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
        print("\n Phonebook")
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
            print("От 0-6...")

    cur.close()
    conn.close()

# Запуск
if __name__ == "__main__":
    menu()
