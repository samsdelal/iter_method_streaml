import streamlit as st

import main


def main_page():
    st.header('Итеративный метод')
    col_1,col_2 = st.columns(2)
    stolb =col_1.number_input('Количество стобцов', step=1, min_value=1, key='stolb')
    stroks = col_2.number_input('Количество строк', step=1, min_value=1, key = 'stork')
    strok = []
    matriz = []
    st.subheader('Платежная матрица')
    for i in st.columns(int(stolb)):
        stolb = []
        for _ in range(1, stroks+1):
            z = i.text_input('', key=f'{_}{i}+1')
            stolb.append(z)
        strok.append(stolb)
    for i in range(len(strok[0])):
        z =[]
        for _ in range(len(strok)):
            z.append(strok[_][i])
        matriz.append(z)
    count_iter = st.number_input('Количество итераций', step=1, min_value=1)
    try:
        main.culc(matriz, int(count_iter))
    except:
        st.subheader('Введены не все значения!')
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
if __name__ == '__main__':
    main_page()
