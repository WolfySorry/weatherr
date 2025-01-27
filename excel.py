from contextlib import contextmanager
import openpyxl
from openpyxl.styles import Alignment

import requests

from apikey import API_KEY


params={"q":'Almaty',"key":API_KEY,'days':'7', "units":"metric"}

response=requests.get( "http://api.weatherapi.com/v1/forecast.json", params=params) # получаем данные от сайта вводя данные сохранненые предварительно в params


status=response.status_code

if status>199:
    print("соединение прошло успешно")

elif status>299:
    print("произошла ошибка")


data=response.json()

n = 0
@contextmanager
def open_excel_file(filename):
    wb = openpyxl.Workbook()    # создаем файл Excel
    ws = wb.active              # а здесь мы сохраняем первый лис в переменной ws с котороый мы будем работать
    
    try:                        # эта функция выполняется пока используется with
        yield ws                # здесь мы уже скажем так "останавливаем время", то есть мы будем использовать то что внутри функции with до того момента как он закончится
                                # и только тогда наша остановка закончится и мы продолжим код с этого момента
    finally:
        wb.save(filename)       # сохраняем в excel


with open_excel_file("weather.xlsx") as ws:
    ws.append(["Date(y,m,d)", "Avg Temp (°C)", "Max Wind (m/s)", "Weather", "Moon Phase"]) # Заполняем заголовок
    ws.append([])
    
    while n < 7:
        first_el = data['forecast']['forecastday'][n]
        date = first_el['date']
        avg_temp = first_el['day']['avgtemp_c']
        maxwind_ms = round(first_el['day']['maxwind_kph']/3.6, 1) # в этих 6 строках мы используем полученные данные из json от нашего api сайта 
        weather = first_el['day']['condition']['text']
        moon_ph = first_el['astro']['moon_phase']
                                                                    
        ws.append([date, avg_temp, maxwind_ms, weather, moon_ph]) # Заполняем таблицу данными
        
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

    for row in ws.iter_rows():   # Перенос текста в ячейках для лучшего отображения
        for cell in row:
            cell.alignment = Alignment(wrap_text=True)


print('Файл сохранен')
