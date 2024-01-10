import psycopg2

class Database():
    def __init__(self, cursor):
        self.cursor = cursor
    
    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS client (
                client_id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(50) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS phone (
                phone_numbers VARCHAR(25) NOT NULL,
                id_client INTEGER REFERENCES client(client_id)
            );
                            """)
        
    def add_info_client(self, name_client: str, last_name_client: str, email: str):
        self.cursor.execute("""
            INSERT INTO client(name, last_name, email)
                VALUES
                (%s, %s, %s);
                """,
                [name_client, last_name_client, email])
        
    def add_phone_client(self, phone_numbers: str, id_client: int):
        self.cursor.execute("""
            INSERT INTO phone
                VALUES
                (%s, %s);
                """,
                [phone_numbers, id_client])
        
    def edit_info_client(self, client_id: int, new_name: str, new_last_name: str, new_email: str):
        for parameter, value in locals().items():
            if value != None:
                if parameter == 'new_name':
                    self.cursor.execute("""
                        UPDATE client
                            SET name = %s
                            WHERE client_id = %s;
                            """,
                            [value, client_id])
                elif parameter == 'new_last_name':
                    self.cursor.execute("""
                        UPDATE client
                            SET last_name = %s
                            WHERE client_id = %s;
                            """,
                            [value, client_id])
                elif parameter == 'new_email':
                    self.cursor.execute("""
                        UPDATE client
                            SET email = %s
                            WHERE client_id = %s;
                            """,
                            [value, client_id])

    def delete_phone_client(self, phone_numbers: str):
        self.cursor.execute("""
            DELETE FROM phone
                WHERE phone_numbers = %s;
                """,
                [phone_numbers])
    
    def delete_client(self, client_id: int):
        self.cursor.execute("""
            SELECT id_client
            FROM phone
            """)
        for phone_exists_id in self.cursor.fetchall():
            if client_id == phone_exists_id[0]:
                deleting_phones_input = input("\nКлиента удалить нельзя, к нему привязан один или несколько номеров телефона. Хотите удалить их сначала?\nY - да,\nN - нет\n")
                if deleting_phones_input.upper() == 'Y':
                    self.cursor.execute("""
                        DELETE FROM phone
                            WHERE id_client = %s;
                        """,
                        [client_id])
                    print('\nТелефоны были успешно удалены')
                return
        
        self.cursor.execute("""
            DELETE FROM client
                WHERE client_id = %s;
                """,
                [client_id])
        
    def find_client(self, name = None, last_name = None, email = None, phone_numbers = None):
        for parameter, value in locals().items():
            if value != None and parameter != 'self':
                if parameter == 'name':
                    self.cursor.execute("""
                        SELECT *
                        FROM client
                        LEFT JOIN phone ON client.client_id = phone.id_client
                        WHERE name = %s;
                        """,
                        [value])
                elif parameter == 'last_name':
                    self.cursor.execute("""
                        SELECT *
                        FROM client
                        LEFT JOIN phone ON client.client_id = phone.id_client
                        WHERE last_name = %s;
                        """,
                        [value])
                elif parameter == 'email':
                    self.cursor.execute("""
                        SELECT *
                        FROM client
                        LEFT JOIN phone ON client.client_id = phone.id_client
                        WHERE email = %s;
                        """,
                        [value])
                elif parameter == 'phone_numbers':
                    self.cursor.execute("""
                        SELECT *
                        FROM client
                        LEFT JOIN phone ON client.client_id = phone.id_client
                        WHERE phone.phone_numbers = %s;
                        """,
                        [value])
                    
                print(self.cursor.fetchall())


if __name__ == '__main__':
    
    with open("password.txt", "r", encoding="UTF-8") as password_file:
        password = password_file.readline()

    connect = psycopg2.connect(dbname="clients", host="localhost", user="postgres", password = password)
    with connect.cursor() as cursor:
        clients_db = Database(cursor)

        while True:
            name_input = None
            last_name_input = None
            email_input = None
            phone_input = None

            user_input = input("\nЧто вы хотите сделать?\n1 - Создать таблицы\n2 - Добавить клиента\n3 - Добавить телефон для клиента\n" + 
                            "4 - Изменить данные о клиенте\n5 - Удалить телефон у клиента\n6 - Удалить клиента\n" + 
                            "7 - Начать поиск клиента\n8 - Выйти\n")
            if user_input == '1':
                clients_db.create_tables()
            elif user_input == '2':
                name_input = input("\nИмя клиента:\n")
                last_name_input = input("Фамилия клиента:\n")
                email_input = input("Email клиента:\n")
                
                clients_db.add_info_client(name_input, last_name_input, email_input)
            elif user_input == '3':
                phone_input = input("\nВведите телефон клиента:\n")
                id_input = input("Введите id клиента:\n")

                clients_db.add_phone_client(phone_input, int(id_input))
            elif user_input == '4':
                id_input = input("\nУкажите id клиента, информация которого подлежит изменению:\n")
                client_input = input("\nЧерез запятую введите цифру того, что вы хотите изменить:\n1 - имя,\n2 - фамилию,\n3 - email\n").split(',')
                for change_number in client_input:
                    if change_number == '1':
                        name_input = input("\nИмя клиента:\n")
                    elif change_number == '2':
                        last_name_input = input("\nФамилия клиента:\n")
                    elif change_number == '3':
                        email_input = input("\nEmail клиента:\n")
                
                clients_db.edit_info_client(int(id_input), name_input, last_name_input, email_input)
            elif user_input == '5':
                phone_input = input("\nУкажите какой телефон вы хотите удалить:\n")

                clients_db.delete_phone_client(phone_input)
            elif user_input == '6':
                client_input = input("\nУкажите id клиента, которого хотите удалить:\n")

                clients_db.delete_client(int(client_input))
            elif user_input == '7':
                client_input = input("\nВведите цифру того, по чему вы хотите начать поиск:\n1 - имя,\n2 - фамилию,\n3 - email,\n4 - телефон\n")
                if client_input == '1':
                    name_input = input("\nИмя клиента:\n")
                    clients_db.find_client(name = name_input)
                elif client_input == '2':
                    last_name_input = input("\nФамилия клиента:\n")
                    clients_db.find_client(last_name = last_name_input)
                elif client_input == '3':
                    email_input = input("\nEmail клиента:\n")
                    clients_db.find_client(email = email_input)
                elif client_input == '4':
                    phone_input = input("\nТелефон клиента:\n")
                    clients_db.find_client(phone_numbers = phone_input)           
            elif user_input == '8':
                break
            else:
                continue

            print("\nДействие успешно сделано👍")
            connect.commit()
            continue

    connect.close()