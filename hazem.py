import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import re
import os
from docx import Document
from docx.shared import Inches
import tempfile
import subprocess





# Кнопки "Разработчики" и "График" для главного выключателя
st.markdown("---")
st.sidebar.markdown("---")
st.sidebar.title("Расчет трудоемкости")
show_upload_button = st.sidebar.checkbox("Разработчики")
# Добавление кнопки для отображения Просмотр каждого разработчика
show_dashboard = st.sidebar.checkbox("Просмотр каждого разработчика")
# st.sidebar.markdown("---")
# Загрузка файла журнала
if show_upload_button:
    image = Image.open("business___team_man_woman_working_together_partner_3d_people_person_service2x.webp")
    st.sidebar.image(image, caption='', use_column_width=True)
    st.write('')
    uploaded_files = st.sidebar.file_uploader("Выберите файл журнала (Log file)", type=['log'])  # Кнопка загрузки файла Log
    if uploaded_files is not None:
        image = Image.open("77.webp")
        new_size = (30, 30)
        resized_image = image.resize(new_size)
        st.sidebar.image(image, caption='', use_column_width=True)  
        # Чтение данных из файла Log
        log_content = uploaded_files.readlines()

        # Преобразуйте содержимое в строки
        lines = [line.decode().strip() for line in log_content]

        # Разделите строки и удалите пустые строки
        lines = [line.strip() for line in lines if line.strip()]

        # Разделите каждую строку на две части с помощью вертикальной черты
        data = [line.split('|')[:2] for line in lines if '|' in line]

        # Создание DataFrame
        df = pd.DataFrame(data, columns=['Дата и время', 'Разработчики'])
        show_upload_button = st.sidebar.checkbox("Общий протокол")
        if show_upload_button:
          st.write('Общий протокол')
          st.write(df)
          st.markdown("---")
        # Применение шаблона к именам пользователей
        pattern = re.compile(r'^[А-Яа-я]+\s[А-Яа-я]+$|^\w+\s\w+$')  
        df = df[df['Разработчики'].apply(lambda x: bool(pattern.match(x.strip())))]  
        
        # Объединение столбцов 'Дата' и 'время' в новый столбец 'Общее время'
        df['Общее время'] = pd.to_datetime(df['Дата и время'], errors='coerce')
        
        # Группировка данных по столбцу 'Разработчики'
        grouped_data = df.groupby('Разработчики')
        
        # Создание пустого списка для хранения результатов (с и без времени отдыха)
        results = []
        cleaned_results = []

        # Вычисление общего времени для каждого разработчика (включая исключение времени отдыха < 30 минут)
        for name, group in grouped_data:
            # Вычисляем разницу во времени
            time_diffs = group['Общее время'].diff().fillna(pd.Timedelta(seconds=0))

            # Исключаем периоды отрицательного времени
            time_diffs = time_diffs[time_diffs >= pd.Timedelta(seconds=0)]

            # Вычисляем общее время после исключения отрицательного времени
            total_time_seconds = time_diffs.sum().total_seconds()

            # Преобразование времени в дни, часы, минуты и секунды
            days, remainder = divmod(total_time_seconds, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Форматирование времени
            formatted_time = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minute, {int(seconds)} seconds"

            # Добавление результатов в список
            results.append({'Разработчики': name, 'Время': formatted_time})

            # Исключаем периоды времени отдыха более 30 минут
            time_diffs = time_diffs[time_diffs <= pd.Timedelta(minutes=30)]

            # Вычисляем общее время после исключения отрицательного времени и времени отдыха
            total_time_seconds = time_diffs.sum().total_seconds()

            # Преобразование времени в дни, часы, минуты и секунды
            days, remainder = divmod(total_time_seconds, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Форматирование времени
            formatted_time = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minute, {int(seconds)} seconds"

            # Добавление результатов в список
            cleaned_results.append({'Разработчики': name, 'Время': formatted_time})
        
        # Создание DataFrame из результатов с и без времени отдыха
        results_df = pd.DataFrame(results)
        cleaned_results_df = pd.DataFrame(cleaned_results)

        # Вывод результатов в виде таблиц
        # st.write('Трудоемкость разработчиков:')
        # st.write(results_df)
        st.write('Трудоемкость разработчиков (без времени отдыха < 30 минут):')
        # st.write(cleaned_results_df)

        # Добавление нового столбца для расчета общего времени в формате "часы и минуты"
        def calculate_total_hours(row):
            time_parts = row['Время'].split(', ')
            total_hours = 0
            total_minutes = 0
            for part in time_parts:
                value, unit = part.split(' ')
                if unit == 'days':
                    total_hours += int(value) * 24
                elif unit == 'hours':
                    total_hours += int(value)
                elif unit == 'minute':
                    total_minutes += int(value)
            total_hours += total_minutes // 60
            total_minutes %= 60
            return f"{total_hours} hours, {total_minutes} minutes"

        # Применяем функцию для расчета общего времени в новом столбце
        cleaned_results_df['Общее количество часов'] = cleaned_results_df.apply(calculate_total_hours, axis=1)

        # Выводим DataFrame с новым столбцом
        st.write(cleaned_results_df)
        image = Image.open("workflow_workspace___office_3d_people_person_team_working_together_work_teamwork2x.webp")
        new_size = (30, 30)
        resized_image = image.resize(new_size)
        st.image(image, caption='', use_column_width=True)
        # Добавление кнопки для отображения Просмотр каждого разработчика
        if show_dashboard:
            st.markdown("---")
            # Получение списка всех имен сотрудников
            developers = cleaned_results_df['Разработчики'].unique()

            # Создание выпадающего списка для выбора сотрудника
            selected_developers = st.multiselect("Выберите разработчиков", developers)

            # Фильтрация данных для выбранных сотрудников
            if selected_developers:
                filtered_data = cleaned_results_df[cleaned_results_df['Разработчики'].isin(selected_developers)]
                for developer in selected_developers:
                    st.write(f"Сводная таблица для {developer}:")
                    st.write(filtered_data[filtered_data['Разработчики'] == developer])
                    
                    
                    
#---------------
#---------------

