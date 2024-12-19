import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk


# Функция для подключения к базе данных
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='8998',
            database='CarRentalSystem'
        )
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Ошибка подключения", str(err))
        return None


# Универсальная функция для получения данных из таблицы
def fetch_table_data(table_name):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return records
    return []


# Универсальная функция для получения информации о столбцах таблицы
def get_table_columns(table_name):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        cursor.close()
        connection.close()
        return [col[0] for col in columns]
    return []


# Универсальная функция для обновления записи
def update_record(table_name, columns, values, record_id):
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            # Создаем SET-часть запроса
            set_clause = ", ".join([f"{col} = %s" for col in columns])
            id_column = get_table_columns(table_name)[0]  # Первая колонка — это ID
            query = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = %s"
            cursor.execute(query, values + [record_id])  # Добавляем значения и ID в конец
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Ошибка базы данных", f"{err}")
            return False
    return False



# Функция для отображения данных таблицы
def show_table_data(tab, table_name):
    columns = get_table_columns(table_name)
    tree = ttk.Treeview(tab, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, stretch=True)

    tree.pack(fill=BOTH, expand=True)

    def load_data():
        for i in tree.get_children():
            tree.delete(i)
        records = fetch_table_data(table_name)
        for record in records:
            tree.insert('', 'end', values=record)

    load_data()

    # Поля для редактирования
    frame = Frame(tab)
    frame.pack(pady=10)

    entry_fields = {}
    for i, col in enumerate(columns[1:], start=1):  # Пропускаем ID
        Label(frame, text=f"{col}:").grid(row=i, column=0)
        entry = Entry(frame)
        entry.grid(row=i, column=1)
        entry_fields[col] = entry

    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            record = tree.item(selected_item)['values']
            for i, col in enumerate(columns[1:], start=1):  # Пропускаем ID
                entry_fields[col].delete(0, END)
                entry_fields[col].insert(0, record[i])

    def save_changes():
        selected_item = tree.selection()
        if selected_item:
            record_id = tree.item(selected_item)['values'][0]  # ID записи
            values = []
            for col in columns[1:]:  # Пропускаем ID
                val = entry_fields[col].get()
                if col.lower().endswith("id") or col.lower() == "year":  # Для числовых колонок
                    if not val.isdigit():
                        messagebox.showerror("Ошибка", f"{col} должен быть числом!")
                        return
                    val = int(val)
                elif "date" in col.lower():  # Для дат
                    try:
                        val = datetime.strptime(val, "%Y-%m-%d").date()
                    except ValueError:
                        messagebox.showerror("Ошибка", f"{col} должен быть в формате YYYY-MM-DD!")
                        return
                values.append(val)
            if update_record(table_name, columns[1:], values, record_id):
                load_data()
                messagebox.showinfo("Успех", "Запись успешно обновлена!")
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить запись.")
        else:
            messagebox.showwarning("Предупреждение", "Выберите запись для редактирования.")

    Button(tab, text="Сохранить изменения", command=save_changes).pack(pady=5)
    tree.bind('<<TreeviewSelect>>', on_tree_select)


# Создание основного окна
root = Tk()
root.title("Управление базой данных CarRentalSystem")
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True)

# Список таблиц
tables = ["Clients", "Employees", "Cars", "RentalContracts", "Payments"]

# Создаем вкладки для каждой таблицы
for table in tables:
    tab = Frame(notebook)
    notebook.add(tab, text=table)
    show_table_data(tab, table)

# Запуск приложения
root.mainloop()
