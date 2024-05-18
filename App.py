#--------------------------------------------------------------------------------------------
#  Импортируйте все библиотеки
import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
import re
import os
# from docx import Document
# from docx.shared import Inches
import tempfile
import subprocess
# import win32com.client
# import tempfile
# import magic
# import openpyxl
#------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------
#  Запустите программу и разместите ее изображение
st.title(" 📊 Project Productivity Professional ")
#10903493.png
image = Image.open("10903493.png")
new_size = (30, 30)
resized_image = image.resize(new_size)
st.image(image, caption='', use_column_width=True)
# st.markdown("---")
st.write('')
# st.sidebar.title('***📊Добро пожаловать📊***')
# st.sidebar.markdown("---")
image = Image.open("Pie_Chart.webp")
new_size = (300, 300)
resized_image = image.resize(new_size)
st.sidebar.image(image, caption='', use_column_width=True)
st.sidebar.markdown("---")
st.sidebar.title("Информация о проекте")
# Установка максимального количества ячеек для отображения в Pandas Styler
pd.set_option("styler.render.max_elements", 559776)
new_size = (300, 300)
resized_image = image.resize(new_size)
#------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------
# Основные характеристики
if st.sidebar.checkbox("Основные характеристики"):
    # st.sidebar.markdown("---")
    selected_dashboards = st.multiselect("Основные характеристики Проекта", ["Основные характеристики"])
    show_fields = st.checkbox("Характеристики проекта ")
    inputs = {}  # Пустой словарь для хранения введенных значений
    if show_fields:
        for dashboard_option in selected_dashboards:
            if dashboard_option == "Основные характеристики":
                inputs["Название Проекта"] = st.text_input("Название Проекта", value="")
                inputs["Адрис Проекта"] = st.text_input("Адрис Проекта", value="")
                inputs["Вид работ"] = st.text_input("Вид работ", value="")
                inputs["Генпроектировщик"] = st.text_input("Генпроектировщик", value="")
                inputs["Номер договора"] = st.text_input("Номер договора", value="")
                inputs["Закачик"] = st.text_input("Закачик", value="")
                inputs["Стадия проекта"] = st.text_input("Стадия Проекта", value="")
                inputs["Назначение Объекта"] = st.text_input("Назначение Объекта", value="")
                inputs["Номер ГПЗУ"] = st.text_input("Номер ГПЗУ", value="")
                inputs["Этажность"] = st.text_input("Этажность", value="")
                inputs["Количество Надземных Этажей"] = st.text_input("Количество Надземных Этажей", value="")
                inputs["Количество Подземных Этажей"] = st.text_input("Количество Подземных Этажей", value="")
                inputs["Количество секций"] = st.text_input("Количество секций", value="")
                inputs["Общая площадь здания m²"] = st.text_input("Общая площадь здания m² ", value="")
                inputs["Строительный Объем m³"] = st.text_input("Строительный Объем m³", value="")  
                inputs["Площадь участка"] = st.text_input("Площадь участка", value="")
                inputs["Полезная площадь"] = st.text_input("Полезная площадь", value="")
    if len(inputs) > 0:  # Просматривайте информационную таблицу только при наличии сохраненных данных
        st.write("***Основные характеристики Проекта:***")
        with st.expander("Показать таблицу"):
            df = pd.DataFrame(inputs.items(), columns=['Имя атрибута', 'Описание'])
           
          
            # st.write(df) 
            st.dataframe(df, width=600)
        




#-------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------
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
          st.dataframe(df, width=600)
          # st.write(df)
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
                                  
#-----------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
show_chart_button = st.sidebar.checkbox("Показать график")
# st.markdown("---")
if show_chart_button:
    # Просмотр параметров для типа диаграммы
    chart_type = st.sidebar.radio("Тип графика ", ("гистограмма", "диаграмма"))

    if chart_type == "гистограмма":
        # Подготовка данных для гистограммы
        bar_data = results_df.copy()
        bar_data['Время'] = pd.to_timedelta(bar_data['Время']).dt.total_seconds() / 3600

        # Создайте столбчатую Штабелированная гистограмма для Общего времени для каждого разработчика
        # fig_bar = px.bar(bar_data, x='Разработчики', y='Время', title='гистограмма для каждого разработчика')
        # # Показать гистограмму
        # st.plotly_chart(fig_bar)

        # Подготовка данных для второй гистограммы
        cleaned_bar_data = cleaned_results_df.copy()
        cleaned_bar_data['Время'] = pd.to_timedelta(cleaned_bar_data['Время']).dt.total_seconds() / 3600

        # Создайте столбчатую Штабелированная гистограмма для Общего времени для каждого разработчика (без времени отдыха < 30 минут)
        fig_cleaned_bar = px.bar(cleaned_bar_data, x='Разработчики', y='Время', title='гистограмма для каждого разработчика (без времени отдыха < 30 минут)')
        # Показать гистограмму
        st.plotly_chart(fig_cleaned_bar)

    elif chart_type == "диаграмма":
        # Подготовьте данные для круговой диаграммы
        pie_data = results_df.copy()
        pie_data['Время'] = pd.to_timedelta(pie_data['Время']).dt.total_seconds()

        # Создайте круговую диаграмму для Общего времени для каждого разработчика
        fig_pie = px.pie(pie_data, values='Время', names='Разработчики', title='диаграмма для каждого разработчика')
        # Задайте значение для изменения расстояния между элементами в круговой окружности
        fig_pie.update_traces(hole=0.3)
        # Показать круговую диаграмму
        # st.plotly_chart(fig_pie)

        # Подготовьте данные для второй круговой диаграммы
        pie_cleaned_data = cleaned_results_df.copy()
        pie_cleaned_data['Время'] = pd.to_timedelta(pie_cleaned_data['Время']).dt.total_seconds()

        # Создайте круговую диаграмму для Общего времени для каждого разработчика (без времени отдыха < 30 минут)
        fig_cleaned_pie = px.pie(pie_cleaned_data, values='Время', names='Разработчики', title='диаграмма для каждого разработчика (без времени отдыха < 30 минут)')
        # Задайте значение для изменения расстояния между элементами в круговой окружности
        fig_cleaned_pie.update_traces(hole=0.3)
        # Показать круговую диаграмму
        st.plotly_chart(fig_cleaned_pie)
        # st.markdown("---")       
#------------------------------------------------------------------------------------------------------------------------------------      
#------------------------------------------------------------------------------------------------------------------------------------      
#------------------------------------------------------------------------------------------------------------------------------------          
# Расчет Количество элементов    
st.sidebar.markdown("---")      
st.sidebar.title("Расчет количества элементов")
if st.sidebar.checkbox("элементов"):
    uploaded_files = st.sidebar.file_uploader("Количества элементов", type=['csv'], accept_multiple_files=True, key='file_uploader', help="Загрузить файлы .csv")
    image = Image.open("csv1.webp")
    new_size = (30, 30)
    resized_image = image.resize(new_size)
    st.sidebar.image(image, caption='', use_column_width=True)

    # Импортируйте данные из каждого файла и добавьте их в список
    if uploaded_files is not None:
        
        all_data = []
        total_sum_all_files = 0  # Общее количество для всех файлов
        
        for file in uploaded_files:
            df = pd.read_csv(file)
            # Основные данные перед анализом
            if 'Количество' not in df.columns:
                df['Количество'] = 1
            sum_values = df['Количество'].sum()
            total_sum_all_files += sum_values  # Добавление к общему количеству
            file_name = file.name.split('.')[0]  # Имя файла без расширения
            data = {
                'Элемент': [file_name],
                'количество': [sum_values]
            }
            df_result = pd.DataFrame(data)
            all_data.append(df_result)
            
        # Объединить все данные в одну таблицу
        if len(all_data) > 0:
            combined_df = pd.concat(all_data, ignore_index=True)
            
            # Создать новый DataFrame для отображения общего количества один раз
            total_df = pd.DataFrame({'Элемент': ['Общее количество'], 'количество': [total_sum_all_files]})
            
            # Добавить общее количество в общую таблицу
            combined_df = pd.concat([combined_df, total_df], ignore_index=True)
            
            # Отображение таблиц
            st.write('Количества элементов:')
            st.write(combined_df)
            # Добавьте кнопку для сохранения таблицы в файле Word
            # if st.button("Сохранение таблицы в файл Word"):
            #     # Создайте файл Word и запишите в него таблицу
            #     document = Document()
                
            #    # Добавьте изображение в верхнюю часть документа
            #     document.add_picture('Урфу.jpg', width=Inches(1.0), height=Inches(1.0))
                
            #     document.add_heading('Таблица элементов', level=1)

            #     # Добавить таблицу
            #     table = document.add_table(rows=combined_df.shape[0]+1, cols=combined_df.shape[1])
            #     # Добавить заголовки
            #     for j in range(combined_df.shape[-1]):
            #         table.cell(0, j).text = combined_df.columns[j]
            #     # Добавить данные
            #     for i in range(combined_df.shape[0]):
            #         for j in range(combined_df.shape[-1]):
            #             table.cell(i+1, j).text = str(combined_df.iloc[i,j])

            #     # Сохраните файл
            #     document.save('таблица элементов.docx')
            #     st.success("Таблица была успешно сохранена в файле Word.")               
#----------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------
#  Спецификации элементов
#----------------------------------------------------------------------------------------------------------------------------------
# загрузка файлов
if st.sidebar.checkbox("Спецификации элементов"):
    uploaded_files = st.sidebar.file_uploader("Импорт файлов CSV", type=['csv'], accept_multiple_files=True)  # кнопка импорта файлов CSV
    

    # использование мультиселекта для выбора нескольких файлов
    selected_files = st.multiselect("Выберите элементов", [file.name for file in uploaded_files] if uploaded_files else [])

    # отображение содержимого для каждого выбранного файла
    for selected_file_name in selected_files:
        # проверка, был ли выбран файл
        if selected_file_name and uploaded_files:
            st.write(f"Спецификации для: {selected_file_name}")

            # получение пути к выбранному файлу
            selected_file_path = [file for file in uploaded_files if file.name == selected_file_name][0]

            # чтение выбранного файла и преобразование его в DataFrame
            selected_df = pd.read_csv(selected_file_path)

            # использование multiselect для отображения списка имен столбцов для каждого файла
            selected_columns = st.multiselect("Выберите категории", selected_df.columns)

            # отображение выбранных данных на основе выбранных столбцов
            if selected_columns:
                st.write(selected_df[selected_columns])
#------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------
#Добавление новой страницы "О программе "
st.sidebar.title("О программе")

if st.sidebar.checkbox("О программе"):
  st.sidebar.write("-  Это программа Была создана командой номер 32 .")
  st.sidebar.write("-  (Главный куратор) -Машкин Олег Владимирович inbox@omashkin.ru ")
  st.sidebar.write("- (Тимлид) - Бадри Хазем Хешам Мухаммед hazim20001@icloud.Com")       
#------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------
#Добавление новой страницы "Renga Api"
if st.sidebar.checkbox("Renga Api"):
    st.sidebar.image("renga.png", width=80, use_column_width=False)
    st.sidebar.markdown("[Открыть](https://help.rengabim.com/api/)")
#------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------
# # #Открыть файл Renga.rnp
# if st.sidebar.checkbox("Открыть файл Renga.rnp"):
#     uploaded_file = st.sidebar.file_uploader("Импорт файла Renga", type=["rnp"])
#     if uploaded_file is not None:
#         # Создание временного каталога, если он не существует
#         temp_dir = tempfile.mkdtemp()
        
#         # Сохранение загруженного файла во временном каталоге
#         file_path = os.path.join(temp_dir, uploaded_file.name)
#         with open(file_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())
        
#         # Открытие файла с использованием приложения по умолчанию, ассоциированного с его расширением
#         try:
#             subprocess.Popen(["xdg-open", file_path])  # Для Linux
#         except FileNotFoundError:
#             try:
#                 subprocess.Popen(["open", file_path])  # Для macOS
#             except FileNotFoundError:
#                 os.startfile(file_path)  # Для Windows
        
#         st.sidebar.success("Файл успешно импортирован и открыт!")
#-----------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
#                ('Калькулятор') 
# Определение, когда показывать калькулятор
show_calculator = st.sidebar.checkbox('Калькулятор')
# Если калькулятор открыт, покажите его
if show_calculator:
    # Выбор арифметической операции
    operation = st.sidebar.selectbox('Выберите арифметическую операцию', ['Сложение (+)', 'Вычитание (-)', 'Умножение (*)', 'Деление (/)', 'Квадратный корень (√)', 'Кубический корень (∛)'])

    # Если пользователь выбрал квадратный корень или кубический корень, покажите только одно поле для ввода числа
    if operation in ['Квадратный корень (√)', 'Кубический корень (∛)']:
        num1 = st.sidebar.number_input('Число', step=1.0)
        num2 = None
    else:
        num1 = st.sidebar.number_input('Первое число')
        num2 = st.sidebar.number_input('Второе число')

    # Показать результат арифметической операции
    if st.sidebar.button('Вычислить'):
        if operation == 'Сложение (+)':
            result = num1 + num2
            st.sidebar.success(f'Результат сложения: {result}')
        elif operation == 'Вычитание (-)':
            result = num1 - num2
            st.sidebar.success(f'Результат вычитания: {result}')
        elif operation == 'Умножение (*)':
            result = num1 * num2
            st.sidebar.success(f'Результат умножения: {result}')
        elif operation == 'Деление (/)':
            if num2 != 0:
                result = num1 / num2
                st.sidebar.success(f'Результат деления: {result}')
            else:
                st.sidebar.error('На ноль делить нельзя')
        elif operation == 'Квадратный корень (√)':
            result = num1 ** 0.5
            st.sidebar.success(f'Квадратный корень из {num1}: {result}')
        elif operation == 'Кубический корень (∛)':
            result = num1 ** (1/3)
            st.sidebar.success(f'Кубический корень из {num1}: {result}')
#-----------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------

#       # ----=-----Путь к журналу   -------


# # Function to handle importing RNP files
# def import_rnp(file_buffer, app):
#     if file_buffer is not None:
#         # Save the uploaded file to a temporary location
#         file_path = tempfile.NamedTemporaryFile(delete=False).name
#         with open(file_path, "wb") as f:
#             f.write(file_buffer.getvalue())

#         # Check if the temporary file exists
#         if os.path.exists(file_path):
#             # Check if the file is a Renga project file
#             file_type = magic.Magic(mime=True).from_file(file_path)
#             if file_type == 'application/octet-stream':
#                 st.error("Invalid file format. Please upload a valid Renga project file.")
#                 return

#             # Open the Renga project
#             app.OpenProject(file_path)
#             project = app.Project
#             if project is not None:
#                 model = project.Model
#                 # Create a DataFrame with project information
#                 data = {
#                     "Attribute": ["Путь к журналу"],
#                     "Value": [project.JournalPath]
#                 }
#                 df = pd.DataFrame(data)
#                 # Display project information in a table
#                 st.write(df)
#             else:
#                 st.error("Failed to open the Renga project.")
#         else:
#             st.error("Failed to upload the file.")

# # Create a Renga application instance
# app = win32com.client.Dispatch("Renga.Application.1")

# # Make the Renga application visible
# app.Visible = True

# # Create a Streamlit sidebar button
# if st.sidebar.checkbox("Где находится журнал .Log"):
#     # Inside the checkbox, create a Streamlit file uploader widget
#     uploaded_file = st.sidebar.file_uploader("Upload RNP file", type=["rnp"])
#     # If file is uploaded, call import_rnp function
#     if uploaded_file is not None:
#         import_rnp(uploaded_file, app)


#-----------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
# Использование флажка для управления отображением раскрывающейся кнопки
st.markdown("---")
if st.sidebar.checkbox("Справка"):
    # Использование раскрывающейся кнопки для отображения содержимого при нажатии на стрелку
    with st.expander("Справка:"):
        # Отображение содержимого внутри раскрывающейся кнопки
        st.write('Какую пользу вы получите от этой программы ?:')
        st.write("- 1-Написаны основные характеристики проекта")
        st.write("- 2-Расчет трудоемкости")
        st.write("- 3-Отображение данных в виде графика")
        st.write("- 4-Расчет количества элементов")
        st.write("- 5-Спецификации элементов")
        st.write("- 6-Открыть файл Renga.RNP")
        st.write("- 7-Идентификатор пути к файлу.LOG")
        st.write("Как работает эта программа?:")
        st.write("- 1-Выберите свой файл в формате журнала.LOG (Для-Расчет трудоемкости)")
        st.write("- 2-Выберите файлы в формате .csv (Для-Расчет количества элементов)")
        st.write("- 3-Выберите файлы в формате .csv (Для-Спецификации элементов)")
        st.write("- 4-Выберите файлы в формате .rnp (Для-Открыть файл Renga)")
        st.write("- 5-Выберите файлы в формате .rnp (Для-Где находится журнал .Log)")
        image = Image.open("Management.webp")
        new_size = (30, 30)
        resized_image = image.resize(new_size)
        st.sidebar.image(image, caption='', use_column_width=True)
        
        
        
#-----------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------

 

 
