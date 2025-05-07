import streamlit as st
import requests
import os

# 🔐 Token Hugging Face desde secrets o variable de entorno
HF_TOKEN = st.secrets.get("HF_TOKEN", os.getenv("HF_TOKEN"))

# ✅ Modelo gratuito y estable
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# Función para consultar la API de Hugging Face
def consultar_modelo(prompt):
    try:
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
        if response.status_code != 200:
            return {"error": f"Código de estado {response.status_code}: {response.text}"}
        result = response.json()
        return result
    except Exception as e:
        return {"error": str(e)}

# Interfaz Streamlit
st.title("🤖 Asistente de Análisis de Software")

apps = st.text_input("📱 Nombre(s) de la(s) aplicación(es):", placeholder="Ej: Replika, Notion")
contexto = st.text_input("🎯 ¿Algún contexto o uso específico?", placeholder="Ej: uso educativo")
tipo = st.radio("🔎 Tipo de análisis", ["Breve", "Completo"])

if st.button("Analizar"):
    if not apps:
        st.warning("Por favor, introduce al menos una aplicación.")
    else:
        prompt = f"""
Actúa como un asistente en castellano experto en análisis de software. 
Usuario ha indicado las siguientes apps: {apps}
Contexto específico: {contexto if contexto else 'Ninguno'}
Desea un análisis tipo: {tipo}

🔁 Instrucciones generales:
- Si el usuario proporciona una sola app, analiza según la estructura detallada.
- Si da varias apps separadas por comas, compáralas al final.
- Adapta el análisis al contexto dado.
- Estructura del análisis:
1. Nombre y categoría
2. Resumen general
3. Instalación y configuración
4. Puntos fuertes
5. Puntos débiles
6. Impacto en la sociedad
7. Sugerencias de mejora
8. Alternativas y comparativa
9. ¿Recomendada?
"""

        with st.spinner("Consultando modelo en Hugging Face..."):
            resultado = consultar_modelo(prompt)
            st.write("🔎 Resultado crudo de la API:", resultado)  # 👁️ Mostrar lo que responde la API

            # Procesar respuesta del modelo
            if "error" in resultado:
                st.error(f"⚠️ Error: {resultado['error']}")
            elif isinstance(resultado, list) and "generated_text" in resultado[0]:
                st.markdown(resultado[0]["generated_text"])
            elif isinstance(resultado, dict) and "generated_text" in resultado:
                st.markdown(resultado["generated_text"])
            else:
                st.error("⚠️ No se pudo procesar la respuesta del modelo.")
