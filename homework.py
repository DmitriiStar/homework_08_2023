import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, mannwhitneyu

st.set_option('deprecation.showPyplotGlobalUse', False) # Без этого - какое-то предупреждение

############### Загрузка ###############
st.title('Анализ данных с помощью Streamlit')

uploaded_file = st.file_uploader("Загрузите CSV файл", type=["csv"])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, encoding='cp1251') # Проблема с юникодом или что-то такое
    st.write('Пример данных:')
    st.dataframe(data.head())

############### Выбор переменных ###############
    columns = data.columns
    col1 = st.selectbox('Выберите первую переменную', columns)
    col2 = st.selectbox('Выберите вторую переменную', columns)

    if col1 != col2:
############### Визуализация распределения ###############
        st.write('## Визуализация распределения')
        fig, ax = plt.subplots(figsize=(10, 6))
        if data[col1].dtype == 'object':
            st.write('### Круговая диаграмма для', col1)
            data[col1].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
        else:
            st.write('### Гистограмма для', col1)
            sns.histplot(data[col1], bins=20, kde=True, ax=ax)
        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(10, 6))
        if data[col2].dtype == 'object':
            st.write('### Круговая диаграмма для', col2)
            data[col2].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
        else:
            st.write('### Гистограмма для', col2)
            sns.histplot(data[col2], bins=20, kde=True, ax=ax)
        st.pyplot(fig)

############### Алгоритм теста гипотез ############### нашел где-то на СтакОверфлоу
        st.write('## Тестирование гипотез')
        test_options = ['t-тест', 'U-тест Манна-Уитни']
        selected_test = st.selectbox('Выберите алгоритм теста гипотез', test_options)

        st.write('### Результаты теста гипотез')
        if data[col1].dtype in ['int64', 'float64'] and data[col2].dtype in ['int64', 'float64']:
            if selected_test == 't-тест':
                result = ttest_ind(data[col1], data[col2])
                st.write('t-статистика:', result.statistic)
                st.write('p-значение:', result.pvalue)
            elif selected_test == 'U-тест Манна-Уитни':
                result = mannwhitneyu(data[col1], data[col2])
                st.write('U-статистика:', result.statistic)
                st.write('p-значение:', result.pvalue)
        else:
            st.write('Тестирование гипотез доступно только для числовых данных.')
    
    else:
        st.write('Выберите разные переменные для анализа.')