from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Функция для подключения к базе данных
def db_connection():
    return pymysql.connect(
        host="localhost",  # Укажите ваш хост
        user="root",       # Укажите имя пользователя
        password="8998",  # Укажите пароль
        database="clothingStore",  # Укажите название базы данных
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

# Главная страница с кнопками
@app.route('/')
def index():
    return render_template('index1.html')

# Маршрут для отображения списка клиентов
@app.route('/customers')  # Изменили маршрут
def customers():
    conn = db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM customers")  # Изменили запрос на получение данных из таблицы customers
                customers_data = cursor.fetchall()  # Изменили название переменной
            conn.close()
            return render_template('customers.html', customers=customers_data)  # Изменили название файла шаблона и переменной
        except pymysql.MySQLError as e:
            print(f"Ошибка MySQL: {e}")
            conn.close()
            return "Ошибка при получении данных"  # Обработка ошибки
    else:
        return "Ошибка подключения к базе данных"  # Обработка ошибки

@app.route('/customers/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        # Получение данных из формы
        customer_name = request.form['customer_name']
        customer_surname = request.form['customer_surname']
        email = request.form.get('email', '')  # Email (опционально)
        address = request.form.get('address', '')  # Адрес (опционально)
        contact_number = request.form.get('contact_number', '')  # Номер телефона (опционально)

        # Подключение к базе данных
        conn = db_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    # SQL-запрос для добавления клиента
                    cursor.execute("""
                        INSERT INTO customers (CustomerName, CustomerSurname, Email, Address, ContactNumber)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (customer_name, customer_surname, email, address, contact_number))
                    conn.commit()
                conn.close()
                return redirect(url_for('customers'))  # Перенаправление на список клиентов
            except pymysql.MySQLError as e:
                print(f"Ошибка MySQL: {e}")
                conn.close()
                return "Ошибка добавления клиента"
        else:
            return "Ошибка подключения к базе данных"

    # Рендеринг шаблона для формы добавления клиента
    return render_template('add_customer.html')

# Страница редактирования клиента
@app.route('/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM customers WHERE CustomerID = %s', (customer_id,))
    customer = cursor.fetchone()

    if request.method == 'POST':
        customer_name = request.form['CustomerName']
        customer_surname = request.form['CustomerSurname']
        contact_number = request.form['ContactNumber']
        email = request.form['Email']
        address = request.form['Address']

        cursor.execute('''
            UPDATE customers
            SET CustomerName = %s, CustomerSurname = %s, ContactNumber = %s, Email = %s, Address = %s
            WHERE CustomerID = %s
        ''', (customer_name, customer_surname, contact_number, email, address, customer_id))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('customers'))

    cursor.close()
    connection.close()
    return render_template('edit_customer.html', customer=customer)

@app.route('/customers/delete/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    conn = db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                # Удаление записи из таблицы customers по ID
                cursor.execute("DELETE FROM customers WHERE CustomerID=%s", (customer_id,))
                conn.commit()
            conn.close()
            return redirect(url_for('customers'))  # Перенаправление на список клиентов
        except pymysql.MySQLError as e:
            print(f"Ошибка MySQL: {e}")
            conn.close()
            return "Ошибка удаления клиента"
    else:
        return "Ошибка подключения к базе данных"

@app.route('/products')  # Изменили маршрут
def products():
    conn = db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM products")  # SQL-запрос к таблице products
                products_data = cursor.fetchall()  # Изменили название переменной
            conn.close()
            return render_template('products.html', products=products_data)  # Изменили название файла шаблона и переменной
        except pymysql.MySQLError as e:
            print(f"Ошибка MySQL: {e}")
            conn.close()
            return "Ошибка при получении данных"  # Обработка ошибки
    else:
        return "Ошибка подключения к базе данных"  # Обработка ошибки

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        price = request.form['price']
        stock = request.form['stock']
        category_id = request.form.get('category_id', None)  # Категория может быть необязательной

        conn = db_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO products (ProductName, Price, Stock, CategoryID)
                        VALUES (%s, %s, %s, %s)
                    """, (product_name, price, stock, category_id))
                    conn.commit()
                    conn.close()
                return redirect(url_for('products'))  # Перенаправление на список продуктов
            except pymysql.MySQLError as e:
                print(f"Ошибка MySQL: {e}")
                conn.close()
                return "Ошибка добавления продукта"
        else:
            return "Ошибка подключения к базе данных"
    return render_template('add_product.html')  # Страница с формой для добавления продукта

@app.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    conn = db_connection()
    if conn:
        try:
            if request.method == 'POST':
                product_name = request.form['product_name']
                price = request.form['price']
                stock = request.form['stock']
                category_id = request.form.get('category_id', None)

                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE products
                        SET ProductName = %s, Price = %s, Stock = %s, CategoryID = %s
                        WHERE ProductID = %s
                    """, (product_name, price, stock, category_id, product_id))
                    conn.commit()
                    conn.close()
                return redirect(url_for('products'))  # Перенаправление на список продуктов
            else:
                # GET запрос для отображения формы редактирования
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM products WHERE ProductID = %s", (product_id,))
                    product = cursor.fetchone()
                conn.close()
                return render_template('edit_product.html', product=product)
        except pymysql.MySQLError as e:
            print(f"Ошибка MySQL: {e}")
            conn.close()
            return "Ошибка редактирования продукта"
    else:
        return "Ошибка подключения к базе данных"

@app.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn = db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM products WHERE ProductID = %s", (product_id,))
                conn.commit()
                conn.close()
            return redirect(url_for('products'))  # Перенаправление на список продуктов
        except pymysql.MySQLError as e:
            print(f"Ошибка MySQL: {e}")
            conn.close()
            return "Ошибка удаления продукта"
    else:
        return "Ошибка подключения к базе данных"

@app.route('/orders')
def orders():
    conn = db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM orders")
                orders_data = cursor.fetchall()  # Извлечение всех данных из таблицы orders
                conn.close()
            return render_template('orders.html', orders=orders_data)  # Отображение данных на странице
        except pymysql.MySQLError as e:
            print(f"Ошибка MySQL: {e}")
            conn.close()
            return "Ошибка при получении данных"
    else:
        return "Ошибка подключения к базе данных"


@app.route('/orders/add', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        order_date = request.form['order_date']
        customer_id = request.form['customer_id']
        employee_id = request.form['employee_id']
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        total_amount = request.form['total_amount']

        conn = db_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO orders (OrderDate, CustomerID, EmployeeID, ProductID, Quantity, TotalAmount)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (order_date, customer_id, employee_id, product_id, quantity, total_amount))
                    conn.commit()
                    conn.close()
                return redirect(url_for('orders'))  # Перенаправление на страницу со всеми заказами
            except pymysql.MySQLError as e:
                print(f"Ошибка MySQL: {e}")
                conn.close()
                return "Ошибка добавления заказа"
        else:
            return "Ошибка подключения к базе данных"
    return render_template('add_order.html')  # Отображение формы добавления заказа


@app.route('/orders/edit/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    conn = db_connection()
    if conn:
        try:
            if request.method == 'POST':
                order_date = request.form['order_date']
                customer_id = request.form['customer_id']
                employee_id = request.form['employee_id']
                product_id = request.form['product_id']
                quantity = request.form['quantity']
                total_amount = request.form['total_amount']

                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE orders
                        SET OrderDate = %s, CustomerID = %s, EmployeeID = %s, ProductID = %s, Quantity = %s, TotalAmount = %s
                        WHERE OrderID = %s
                    """, (order_date, customer_id, employee_id, product_id, quantity, total_amount, order_id))
                    conn.commit()
                    conn.close()
                return redirect(url_for('orders'))
            else:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM orders WHERE OrderID = %s", (order_id,))
                    order = cursor.fetchone()  # Получаем данные конкретного заказа
                conn.close()
                return render_template('edit_order.html', order=order)
        except pymysql.MySQLError as e:
            print(f"Ошибка MySQL: {e}")
            conn.close()
            return "Ошибка редактирования заказа"
    else:
        return "Ошибка подключения к базе данных"

@app.route('/orders/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    conn = db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM orders WHERE OrderID=%s", (order_id,))
                conn.commit()
            conn.close()
            return redirect(url_for('orders'))
        except pymysql.MySQLError as e:
            print(f"Ошибка MySQL: {e}")
            conn.close()
            return "Ошибка удаления заказа"
    else:
        return "Ошибка подключения к базе данных"

# Главная страница списка сотрудников
@app.route('/employees')
def employees():
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employees")
    employees_data = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('employees.html', employees=employees_data)

# Добавление нового сотрудника
@app.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        employee_name = request.form['employee_name']
        employee_surname = request.form['employee_surname']
        position = request.form['position']
        contact_number = request.form['contact_number']

        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO employees (EmployeeName, EmployeeSurname, Position, ContactNumber) 
            VALUES (%s, %s, %s, %s)
        """, (employee_name, employee_surname, position, contact_number))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('employees'))
    return render_template('add_employee.html')

# Редактирование сотрудника
@app.route('/employees/edit/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    connection = db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        employee_name = request.form['employee_name']
        employee_surname = request.form['employee_surname']
        position = request.form['position']
        contact_number = request.form['contact_number']

        cursor.execute("""
            UPDATE employees
            SET EmployeeName = %s, EmployeeSurname = %s, Position = %s, ContactNumber = %s
            WHERE EmployeeID = %s
        """, (employee_name, employee_surname, position, contact_number, employee_id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('employees'))

    # Получение данных о сотруднике для редактирования
    cursor.execute("SELECT * FROM employees WHERE EmployeeID = %s", (employee_id,))
    employee = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit_employee.html', employee=employee)

# Удаление сотрудника
@app.route('/employees/delete/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM employees WHERE EmployeeID = %s", (employee_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('employees'))

# Главная страница категорий
@app.route('/categories')
def categories():
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM categories")
    categories_data = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('categories.html', categories=categories_data)

# Добавление новой категории
@app.route('/categories/add', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        category_name = request.form['CategoryName']
        description = request.form['Description']

        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO categories (CategoryName, Description) VALUES (%s, %s)",
            (category_name, description)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('categories'))
    return render_template('add_category.html')

# Редактирование категории
@app.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    connection = db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        category_name = request.form['CategoryName']
        description = request.form['Description']

        cursor.execute(
            "UPDATE categories SET CategoryName = %s, Description = %s WHERE CategoryID = %s",
            (category_name, description, category_id)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('categories'))

    cursor.execute("SELECT * FROM categories WHERE CategoryID = %s", (category_id,))
    category = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit_category.html', category=category)

# Удаление категории
@app.route('/categories/delete/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM categories WHERE CategoryID = %s", (category_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('categories'))

if __name__ == '__main__':
    app.run(debug=True)
