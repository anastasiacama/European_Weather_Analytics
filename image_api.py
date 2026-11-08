
import requests
import streamlit as st


def get_city_image(city): # funzione che cerca la fotografa della città
    url = "https://api.unsplash.com/search/photos"

    headers = { # chiave per l'accesso
        "Authorization": (
            f"Client-ID {st.secrets['UNSPLASH_ACCESS_KEY']}"
        )
    }

    params = {
        "query": f"{city} city skyline landmark",
        "per_page": 1,
        "orientation": "landscape"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    results = response.json()["results"]

    if not results:
        return None

    photo = results[0]

    return {
        "image_url": photo["urls"]["regular"],
        "photographer": photo["user"]["name"],
        "photographer_url": photo["user"]["links"]["html"],
        "photo_url": photo["links"]["html"]
    }
