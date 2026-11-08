
# comunica con le API metereologiche, recupera i dati e li trasforma in un dataframe

import requests # libreria che permette di effettuare richieste http verso API e siti web
import pandas as pd
import streamlit as st

@st.cache_data(ttl=3600) # decoratore di Streamlit che serve a memorizzare temporaneamente il risultato di una funzione, evitando di eseguire ogni volta operazioni che sono già state effettuate

# definisco la funzione che dal nome della città mi danno le coordinate
def get_coordinates(city):
    url = "https://geocoding-api.open-meteo.com/v1/search" # URL dell'API di geolocalizzazione di Open-Meteo -> coordinate geografiche

    params = { # dizionario: nome città, num max ris, lingua ris, formato risp
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    # invio la richiesta get all'API: dove inviare la richiesta, parametri, tempo massimo per ricevere risposta [s]
    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status() # controllo se la richiesta è andata a buon fine

    results = response.json().get("results", []) # (prima parte) converto la risposta in strutture python (seconda) recupero i risultati della ricerca

    if not results:
        raise ValueError(f"City not found: {city}")

    location = results[0] # considero il primo risultato

    return (
        location["latitude"],
        location["longitude"],
        location["name"],
        location.get("country_code", ""), # codice del paese
        location.get("country", "") # nome del paese
    )

@st.cache_data(ttl=3600)

# definisco la funzione principale
def get_weather(city, start_date, end_date):
    latitude, longitude, city_name, country_code, country = get_coordinates(city)

    url = "https://archive-api.open-meteo.com/v1/archive" # utilizziamo l'API Archive di Open-Meteo -> dati metereologici storici

    params = { # dizionario
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": [ # specifico quali info ottenere: T mean, T max, T min, precip tot, pioggia tot, ore di precip, vel max vento, vel min ven, umidità rel mean, durata sole, radiazione sol, codice condizione metereologica
            "temperature_2m_mean",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "rain_sum",
            "precipitation_hours",
            "wind_speed_10m_max",
            "wind_speed_10m_mean",
            "relative_humidity_2m_mean",
            "sunshine_duration",
            "shortwave_radiation_sum",
            "weather_code"
        ],
        "timezone": "auto" # determina automaticamente il fuso orario della località
    }

    # invio richiesta e ottengo dati
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status() # controllo

    data = response.json() # converto in strutture python

    # verifica che la risposta contenga effettivamente i valori giornalieri
    if "daily" not in data:
        raise ValueError("Weather data unavailable.")

    # trasformo i dati in un DataFrame
    df = pd.DataFrame(data["daily"])
    df["time"] = pd.to_datetime(df["time"]) # converto la colonna time da stringhe a date riconosciute da Pandas

    return city_name, country_code, country, df
