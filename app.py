import streamlit as st
import requests
import os

# Token Hugging Face
HF_TOKEN = st.secrets.get("HF_TOKEN", os.getenv("HF_TOKEN"))
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# Función para consultar el modelo
def consultar_modelo(prompt):
    try:
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt}, timeout=45)
        if response.status_code != 200:
            return {"error": f"Código de estado {response.status_code}: {response.text}"}
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Interfaz Streamlit
st.title("Asistente de Análisis de Software")

apps = st.text_input(" Nombre(s) de la(s) aplicación(es):", placeholder="Ej: Replika, Notion")
contexto = st.text_input(" ¿Algún contexto o uso específico?", placeholder="Ej: enseñanza de idiomas, productividad")
tipo = st.radio(" Tipo de análisis", ["Breve", "Completo"])

if st.button("Analizar"):
    if not apps and not contexto:
        st.warning("Por favor, introduce al menos una aplicación o un contexto.")
    else:
        # Prompt para análisis de apps
        if apps:
            prompt = f"""
Actúa como un asistente en castellano experto en análisis de software. 
Usuario ha indicado las siguientes apps: {apps}
Contexto específico: {contexto if contexto else 'Ninguno'}
Desea un análisis tipo: {tipo}

Instrucciones generales:
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
        # Prompt para recomendaciones por contexto
        else:
            prompt = f"""
Actúa como un asistente en castellano experto en análisis de software.
El usuario no ha especificado ninguna aplicación, pero sí un contexto de uso: "{contexto}".
Tu tarea es recomendarle las mejores aplicaciones disponibles actualmente para ese caso,
explicando brevemente qué hace cada una, sus ventajas y en qué situaciones se destaca.
Al final, sugiere cuál es la mejor opción según lo descrito.

Estructura sugerida:
1. Recomendaciones principales (nombre y descripción breve)
2. Comparativa de ventajas
3. Recomendación final con justificación
"""

        # Llamada al modelo
        with st.spinner("Consultando modelo en Hugging Face..."):
            resultado = consultar_modelo(prompt)
            if "error" in resultado:
                st.error(f" Error: {resultado['error']}")
            elif isinstance(resultado, list) and "generated_text" in resultado[0]:
                st.markdown(resultado[0]["generated_text"])
            elif isinstance(resultado, dict) and "generated_text" in resultado:
                st.markdown(resultado["generated_text"])
            else:
                st.error(" No se pudo procesar la respuesta del modelo.")
