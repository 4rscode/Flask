import pandas as pd
import xlsxwriter
from scipy.optimize import linprog


def create_transportation_excel():
    # Данные задачи
    cost = [
        [8, 7, 10, 3, 6, 4],
        [13, 13, 8, 11, 9, 7],
        [14, 8, 11, 9, 6, 5],
        [12, 6, 14, 10, 12, 9],
        [10, 9, 12, 14, 13, 6]
    ]  # Стоимости перевозки

    supply = [240, 180, 360, 180, 150]  # Производство на заводах
    demand = [230, 220, 130, 170, 190, 110]  # Потребность объектов

    # Проверка баланса
    total_supply = sum(supply)
    total_demand = sum(demand)
    if total_supply > total_demand:
        # Добавляем фиктивного потребителя
        demand.append(total_supply - total_demand)
        for row in cost:
            row.append(0)  # Стоимость перевозки к фиктивному потребителю = 0
    elif total_demand > total_supply:
        # Добавляем фиктивного производителя
        supply.append(total_demand - total_supply)
        cost.append([0] * len(demand))  # Стоимость перевозки от фиктивного производителя = 0

    # Преобразование данных в формат для линейного программирования
    c = [item for sublist in cost for item in sublist]  # Вектор стоимостей
    A_eq = []
    b_eq = supply + demand

    # Ограничения по поставкам
    for i in range(len(supply)):
        row = [0] * len(c)
        for j in range(len(demand)):
            row[i * len(demand) + j] = 1
        A_eq.append(row)

    # Ограничения по потребностям
    for j in range(len(demand)):
        row = [0] * len(c)
        for i in range(len(supply)):
            row[i * len(demand) + j] = 1
        A_eq.append(row)

    # Решение задачи линейного программирования
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method='highs')

    # Проверка успеха решения
    if result.success:
        # Получение результатов в удобном формате
        x = result.x.reshape(len(supply), len(demand))
        total_cost = result.fun

        # Создание Excel-файла
        writer = pd.ExcelWriter("optimal_transport_plan.xlsx", engine="xlsxwriter")

        # Таблица перевозок
        df_plan = pd.DataFrame(x, columns=[f"Object {i+1}" for i in range(len(demand))],
                               index=[f"Factory {i+1}" for i in range(len(supply))])
        df_plan.to_excel(writer, sheet_name="Transport Plan")

        # Общая стоимость
        df_cost = pd.DataFrame([[total_cost]], columns=["Total Cost"])
        df_cost.to_excel(writer, sheet_name="Summary", index=False)

        writer._save()
        print("Excel-файл с оптимальным планом создан: optimal_transport_plan.xlsx")
    else:
        print("Решение не найдено. Проверьте входные данные.")

# Вызов функции
create_transportation_excel()
