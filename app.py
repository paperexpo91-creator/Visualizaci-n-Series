import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

st.title("Gráfica de series de tiempo")

entrada = st.text_input("Ingrese la serie, separada por comas:", value="10,15,18,26,31")

try:
    serie = [float(x.strip()) for x in entrada.split(",")]
    
    # Mostrar estadísticas
    col1, col2, col3 = st.columns(3)
    col1.metric("Promedio", f"{sum(serie)/len(serie):.2f}")
    col2.metric("Máximo", max(serie))
    col3.metric("Mínimo", min(serie))
    
    # Selecciona el tipo de gráfica
    tipo = st.selectbox("Tipo de gráfica:", ["Línea", "Área", "Barras"])
    
    # Calcular línea de tendencia y proyección
    X = np.array(range(len(serie))).reshape(-1, 1)
    y = np.array(serie)
    
    modelo = LinearRegression()
    modelo.fit(X, y)
    
    # Proyectar 6 períodos futuros
    X_futuro = np.array(range(len(serie), len(serie) + 6)).reshape(-1, 1)
    y_futuro = modelo.predict(X_futuro)
    
    # Crear gráfica con Plotly (según tipo seleccionado)
    fig = go.Figure()
    
    # Línea de tendencia histórica
    y_tendencia = modelo.predict(X)
    
    # Proyección futura
    x_proyeccion = list(range(len(serie)-1, len(serie) + 6))
    y_proyeccion = list([serie[-1]]) + list(y_futuro)
    
    if tipo == "Línea":
        # Datos originales
        fig.add_trace(go.Scatter(
            x=list(range(len(serie))),
            y=serie,
            mode='lines+markers',
            name='Datos reales',
            line=dict(color='blue', width=2),
            marker=dict(size=8)
        ))
        
        # Tendencia
        fig.add_trace(go.Scatter(
            x=list(range(len(serie))),
            y=y_tendencia,
            mode='lines',
            name='Tendencia',
            line=dict(color='orange', width=2, dash='dash')
        ))
        
        # Proyección
        fig.add_trace(go.Scatter(
            x=x_proyeccion,
            y=y_proyeccion,
            mode='lines+markers',
            name='Proyección (6 períodos)',
            line=dict(color='red', width=2, dash='dot'),
            marker=dict(size=6)
        ))
    
    elif tipo == "Área":
        # Datos originales (con área)
        fig.add_trace(go.Scatter(
            x=list(range(len(serie))),
            y=serie,
            mode='lines+markers',
            name='Datos reales',
            line=dict(color='blue', width=2),
            fill='tozeroy',
            marker=dict(size=8)
        ))
        
        # Tendencia
        fig.add_trace(go.Scatter(
            x=list(range(len(serie))),
            y=y_tendencia,
            mode='lines',
            name='Tendencia',
            line=dict(color='orange', width=2, dash='dash')
        ))
        
        # Proyección
        fig.add_trace(go.Scatter(
            x=x_proyeccion,
            y=y_proyeccion,
            mode='lines+markers',
            name='Proyección (6 períodos)',
            line=dict(color='red', width=2, dash='dot'),
            marker=dict(size=6)
        ))
    
    else:  # Barras
        # Datos originales (barras)
        fig.add_trace(go.Bar(
            x=list(range(len(serie))),
            y=serie,
            name='Datos reales',
            marker=dict(color='blue')
        ))
        
        # Tendencia (línea sobre barras)
        fig.add_trace(go.Scatter(
            x=list(range(len(serie))),
            y=y_tendencia,
            mode='lines',
            name='Tendencia',
            line=dict(color='orange', width=2, dash='dash')
        ))
        
        # Proyección (línea)
        fig.add_trace(go.Scatter(
            x=x_proyeccion,
            y=y_proyeccion,
            mode='lines+markers',
            name='Proyección (6 períodos)',
            line=dict(color='red', width=2, dash='dot'),
            marker=dict(size=6)
        ))
    
    # Diseño
    fig.update_layout(
        title="Serie de tiempo con tendencia y proyección",
        xaxis_title="Período",
        yaxis_title="Valor",
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar tabla de datos
    st.subheader("📊 Tabla de datos")
    df = pd.DataFrame({
        "Índice": range(len(serie)),
        "Valor": serie
    })
    st.dataframe(df, use_container_width=True)
    
    # Mostrar proyecciones
    st.subheader("🔮 Proyecciones para los próximos 6 períodos")
    df_proyecciones = pd.DataFrame({
        "Período": range(len(serie), len(serie) + 6),
        "Valor proyectado": [f"{v:.2f}" for v in y_futuro]
    })
    st.dataframe(df_proyecciones, use_container_width=True)
        
except ValueError:
    st.error("❌ Error: Ingresa números separados por comas (ej: 10,15,18,26,31)")