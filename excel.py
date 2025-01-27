from contextlib import contextmanager
import openpyxl
from openpyxl.styles import Alignment

import requests

from apikey import API_KEY


params={"q":'Almaty',"key":API_KEY,'days':'7', "units":"metric"}

response=requests.get( "http://api.weatherapi.com/v1/forecast.json", params=params)


status=response.status_code

if status>199:
    print("соединение прошло успешно")

elif status>299:
    print("произошла ошибка")


data=response.json()



headers = ['Дата','Средняя температура(°C)','Скорость ветра (км\час)','Погода', 'Фаза Луны']



table = []

n = 0
@contextmanager
def open_excel_file(filename):
    wb = openpyxl.Workbook()
    ws = wb.active
    try:
        yield ws  # Возвращаем рабочий лист
    finally:
        wb.save(filename)


with open_excel_file("weather.xlsx") as ws:
    ws.append(["Date(y,m,d)", "Avg Temp (°C)", "Max Wind (m/s)", "Weather", "Moon Phase"])
    ws.append([])
    while n < 7:
        first_el = data['forecast']['forecastday'][n]
        date = first_el['date']
        avg_temp = first_el['day']['avgtemp_c']
        maxwind_ms = round(first_el['day']['maxwind_kph']/3.6, 1)
        weather = first_el['day']['condition']['text']
        moon_ph = first_el['astro']['moon_phase']
            # Заполняем таблицу данными
        ws.append([date, avg_temp, maxwind_ms, weather, moon_ph])
        n = n + 1
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter  # Получаем букву столбца (например, 'A', 'B', 'C' и т.д.)

        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = max_length + 2  # Увеличиваем ширину для читаемости
        ws.column_dimensions[column].width = adjusted_width

        # Перенос текста в ячейках для лучшего отображения
    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = Alignment(wrap_text=True)




print('Файл сохранен')