import streamlit as st
import json
from typing import Optional
import requests

# Fonction pour exécuter le flow
def run_flow(message: str,
             endpoint: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             api_key: Optional[str] = None) -> dict:
    BASE_API_URL = "https://yellow-br1cks-langflow-test-acr.hf.space"
    api_url = f"{BASE_API_URL}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }

    headers = {}
    if tweaks:
        payload["tweaks"] = tweaks
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Fonction pour extraire les informations pertinentes
def extract_response_details(response: dict) -> str:
    try:
        # Accéder au texte principal
        text = response["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
        sender = response["outputs"][0]["outputs"][0]["results"]["message"]["data"]["sender"]
        timestamp = response["outputs"][0]["outputs"][0]["results"]["message"]["data"]["timestamp"]

        # Formater la réponse
        formatted_response = f"**Réponse de {sender} :**\n\n{text}\n\n**Date et heure :** {timestamp}"
        return formatted_response
    except KeyError:
        return "Impossible d'extraire les informations pertinentes de la réponse."

# Configuration Streamlit
st.title('Application Streamlit avec Langflow en backend')

# Champs pour l'entrée utilisateur
user_input = st.text_input('Entrez votre message :')
endpoint = st.text_input('Entrez le nom de l\'endpoint :', value='POC_RAG_ACR')
api_key = st.text_input('Entrez votre clé API (si nécessaire) :', type='password')

# Bouton pour envoyer la requête
if st.button('Envoyer'):
    with st.spinner('Traitement en cours...'):
        try:
            # Envoyer la requête
            response = run_flow(
                message=user_input,
                endpoint=endpoint,
                api_key=api_key
            )

            # Extraire les détails
            response_text = extract_response_details(response)

            # Afficher la réponse formatée
            st.success('Réponse reçue :')
            st.markdown(response_text)

        except requests.exceptions.HTTPError as http_err:
            st.error(f'Erreur HTTP : {http_err}')
        except Exception as e:
            st.error(f'Une erreur est survenue : {e}')
