import streamlit as st

st.title('Gráfica de barra de tiempo')

entrada = st.text_input('Ingrese la serie separada por comas', value = "15,20,40,45,20")
entrada2= entrada.split(',')

serie = [float(i) for i in entrada2]

st.line_chart(serie)