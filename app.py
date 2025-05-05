import streamlit as st
import requests
import os

HF_TOKEN = st.secrets.get("HF_TOKEN", os.getenv("HF_TOKEN"))
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3-3.3-70B-Instruct"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def consultar_modelo(prompt):
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    try:
        return response.json()[0]["generated_text"]
    except:
        return "⚠️ Error al procesar la respuesta del modelo."

st.title("🤖 Asistente de Análisis de Software")

apps = st.text_input("📱 Nombre(s) de la(s) aplicación(es):")
contexto = st.text_input("🎯 ¿Algún contexto o uso específico?")
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
        with st.spinner("Consultando modelo LLaMA en Hugging Face..."):
            salida = consultar_modelo(prompt)
            st.markdown(salida)
