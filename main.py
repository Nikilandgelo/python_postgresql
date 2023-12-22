import psycopg2

class Database():
    def __init__(self, cursor):
        self.cursor = cursor

    def delete_tables(self):
        self.cursor.execute("""
            DROP TABLE IF EXISTS phone, client;
                            """)
    
    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS client (
                client_id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(50) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS phone (
                phone_numbers VARCHAR(25),
                id_client INTEGER REFERENCES client(client_id)
            );
                            """)
        
    def add_info_client(self, name_client: str, last_name_client: str, email: str):
        self.cursor.execute(f"""
            INSERT INTO client(name, last_name, email)
                VALUES
                ('{name_client}', '{last_name_client}', '{email}');
                             """)
        
    def add_phone_client(self, phone_numbers: str, id_client: int):
        self.cursor.execute(f"""
            INSERT INTO phone
                VALUES
                ('{phone_numbers}', '{id_client}');
                             """)
    
    def edit_one_info_client(self, id_client: int, need_change: str, changed_value: str):
        self.cursor.execute(f"""
            UPDATE client
                SET {need_change} = '{changed_value}'
                WHERE client_id = {id_client};
                             """)
        
    def edit_full_info_client(self, id_client: int, new_name: str, new_last_name: str, new_email: str):
        self.cursor.execute(f"""
            UPDATE client
                SET name = '{new_name}', last_name = '{new_last_name}', email = '{new_email}'
                WHERE client_id = {id_client};
                             """)
    
    def delete_phone_client(self, phone_numbers: str):
        self.cursor.execute(f"""
            DELETE FROM phone
                WHERE phone_numbers = '{phone_numbers}';
                             """)
    
    def delete_client(self, client_id: int):
        self.cursor.execute(f"""
            DELETE FROM client
                WHERE client_id = {client_id};
                             """)
        
    def find_client(self, name = None, last_name = None, email = None, phone_numbers = None):
        filter_string = ''
        is_first_filter = True

        for parameter, value in locals().items():
            if parameter in ('name', 'last_name', 'email', 'phone_numbers') and value != None:
                if is_first_filter == True:
                    filter_string += f"{parameter} = '{value}'"
                    is_first_filter = False
                else:
                    filter_string += f" AND {parameter} = '{value}'"

        self.cursor.execute(f"""
            SELECT *
            FROM client
            JOIN phone ON client.client_id = phone.id_client
            WHERE {filter_string};
                             """)
        print(self.cursor.fetchone())

password_file = open("password.txt", "r", encoding="UTF-8").readline()

connect = psycopg2.connect(dbname="clients", host="localhost", user="postgres", password = password_file)
cursor = connect.cursor()
clients_db = Database(cursor)

with cursor as doesnt_matter:
    while True:
        user_input = input("\nЧто вы хотите сделать?\n1 - Создать таблицы\n2 - Добавить клиента\n3 - Добавить телефон для клиента\n" + 
                           "4 - Изменить данные о клиенте\n5 - Удалить телефон у клиента\n6 - Удалить клиента\n" + 
                           "7 - Начать поиск клиента\n8 - Удалить таблицы\n9 - Выйти\n")
        if user_input == '1':
            clients_db.create_tables()
        elif user_input == '2':
            client_input = input("Через запятую введите имя, фамилию и email клиента:\n").split(",")
            clients_db.add_info_client(client_input[0], client_input[1], client_input[2])
        elif user_input == '3':
            phone_input = input("Через запятую введите телефон и id клиента:\n").split(",")
            clients_db.add_phone_client(phone_input[0], int(phone_input[1]))
        elif user_input == '4':
            yes_no_input = input("Вы хотите полностью изменить данные о клиенте? Y/N\n").strip()
            if yes_no_input.upper() == 'Y':
                client_input = input("Через запятую введите id, имя, фамилию и email клиента:\n").split(",")
                clients_db.edit_full_info_client(int(client_input[0]), client_input[1], client_input[2], client_input[3])
            else:
                client_input = input("Через запятую введите id, что именно изменять(name, last_name, email) и новое значение:\n").split(",")
                clients_db.edit_one_info_client(int(client_input[0]), client_input[1], client_input[2])
        elif user_input == '5':
            phone_input = input("Укажите какой телефон вы хотите удалить:\n").strip()
            clients_db.delete_phone_client(phone_input)
        elif user_input == '6':
            client_input = input("Укажите id клиента, которого хотите удалить:\n").strip()
            clients_db.delete_client(int(client_input))
        elif user_input == '7':
            print("Здесь я не придумал как интерактивно можно реализовать поиск по клиентам и я вообще не уверен нужно ли все это, " +
                               "но поиск можно сделать так:\n'clients_db.find_client(name='Илья', phone_numbers='5558464')' - это если несколько\n" +
                               "'clients_db.find_client(last_name='Редькин')' - это если один аргумент")
            
            # clients_db.find_client(name='Илья')                         # при двух ильях будет только верхний очевидно
            # clients_db.find_client(name='Илья', last_name='Редькин')    # так можно попытаться найти более конкретного
            ok = input("OK... (что угодно введите)\n")
        elif user_input == '8':
            clients_db.delete_tables()
        elif user_input == '9':
            break

        print("\nДействие успешно сделано👍")
        connect.commit()
        continue

connect.close()