
# gestisce l'interfaccia grafica, gli input dell'utente, i grafici e la visualizzazione dati

import streamlit as st # crea l'interfaccia web
import pandas as pd
import matplotlib.pyplot as plt

# librerie standard di Python
from datetime import date
from calendar import monthrange
from io import BytesIO

import folium # per creare mappe geografiche e aggiungere i marcatori per la città
from streamlit_folium import st_folium # per integrare la mappa folium in streamlit

# librerie per creare il pdf
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from weather_api import get_weather, get_coordinates # importa le mie funzioni
from image_api import get_city_image


# configurazione pagina
st.set_page_config(
    page_title="European Weather Analytics",
    page_icon="🌍",
    layout="wide" # pagina più larga
)

# visualizza il titolo principale
st.title("🌍 European Weather Analytics")
# visualizza una descrizione in stile markdown
st.markdown(
    "Explore historical weather data across European capitals."
)

# creazione della barra laterale
st.sidebar.header("Search weather data") # intestazione

city = st.sidebar.text_input( # creo un campo di testo
    "Enter a European capital",
    value="Paris" # valore di default
)

# Opzione: comparazione di due città
compare_cities = st.sidebar.checkbox( 
    "Compare two cities"
)
if compare_cities:
    city2 = st.sidebar.text_input(
        "Second capital",
        value="Rome"
    )
else:
    city2 = None

# Opzione: confronto tra anni diversi
compare_years = st.sidebar.checkbox(
    "Compare two different years"
)
if compare_years:
    year2 = st.sidebar.number_input(
        "Second year",
        min_value=1940,
        max_value=date.today().year,
        value=2023
    )
else:
    year2 = None

search_type = st.sidebar.radio( # radio indica un elemento dell'interfaccia grafica detto radio button, serve per permettere di selezionare solo una opzione tra le alternative
    "Select search type",
    ["Entire year", "Specific month"]
)

year = st.sidebar.number_input( # creo un campo numerico per selezionare l'anno
    "Year",
    min_value=1940,
    max_value=date.today().year,
    value=2024 # recupero la data di oggi
)

# nel caso si selezioni un mese specifico
if search_type == "Specific month":
    month = st.sidebar.selectbox( # menu a tendina con i mesi
        "Month",
        range(1, 13), # da 1 a 12
        # lambda funzione definita senza dare un nome
        format_func=lambda x: date(2000, x, 1).strftime("%B") # strftime trasforma il numero del mese nel nome del mese
    )

    start_date = date(int(year), month, 1) # individua il primo giorno del mese
    end_date = date( # individua l'ultimo giorno del mese
        int(year),
        month,
        monthrange(int(year), month)[1] # perchè i mesi hanno lunghezze diverse
    )
else: # se invece seleziono l'intero anno
    start_date = date(int(year), 1, 1)
    end_date = date(int(year), 12, 31)

# pulsante di ricerca, eseguo tutto il codice
if st.sidebar.button("Get Weather Data", type="primary"):
        # controlli
        if start_date > date.today():
            st.error("The selected period is in the future.")

        elif end_date > date.today():
            st.error("The selected period is not entirely in the past.")

        elif compare_cities and not city2.strip():
            st.error("Please enter the second city.")

        elif compare_cities and city.strip().lower() == city2.strip().lower():
            st.error("Please enter two different cities.")

        elif compare_years and int(year2) == int(year):
            st.error("Please select two different years.")

        else:
            try: # codice che simula un errore
                with st.spinner("Retrieving weather data..."): # mostra un messaggio di caricamento mentre il programma lavora

                    # connessione tra i due codici scritti
                    city_name, country_code, country, df = get_weather(
                        city,
                        start_date.isoformat(), # isoformat converte una data python in una stringa
                        end_date.isoformat()
                    )

                    # Se è attivo il confronto tra due città
                    if compare_cities:
                        # Recupero i dati della seconda città
                        city_name2, country_code2, country2, df2 = get_weather(
                            city2,
                            start_date.isoformat(),
                            end_date.isoformat()
                        )

                    # Se è attivo il confronto tra due anni
                    if compare_years:
                       # Recupero i dati del secondo anno
                        if search_type == "Specific month":
                            start_date2 = date(int(year2), month, 1)
                            end_date2 = date(
                                int(year2),
                                month,
                                monthrange(int(year2), month)[1]
                            )
                        else:
                            start_date2 = date(int(year2), 1, 1)
                            end_date2 = date(int(year2), 12, 31)

                        # Evito di richiedere dati futuri
                        if end_date2 > date.today():
                            end_date2 = date.today()

                        city_name_year, country_code_year, country_year, df_year = get_weather(
                            city,
                            start_date2.isoformat(),
                            end_date2.isoformat()
                        )

                # Salvo i risultati nella sessione: Streamlit li conserva anche quando l'utente clicca su download o interagisce con la pagina.
                st.session_state["weather_results"] = {
                    "city_name": city_name,
                    "country_code": country_code,
                    "country": country,
                    "df": df,
                    "compare_cities": compare_cities,
                    "compare_years": compare_years,
                    "city2": city2,
                    "year": int(year),
                    "year2": int(year2) if compare_years else None,
                    "search_type": search_type,
                    "month": month if search_type == "Specific month" else None,
                    "start_date": start_date,
                    "end_date": end_date,
                    "city_name2": city_name2 if compare_cities else None,
                    "country_code2": country_code2 if compare_cities else None,
                    "country2": country2 if compare_cities else None,
                    "df2": df2 if compare_cities else None,
                    "df_year": df_year if compare_years else None
                }

            except Exception as error: # se qualcosa va storto
                st.error(f"An error occurred: {error}")

# Visualizzo i risultati salvati, anche dopo i successivi aggiornamenti della pagina.
if "weather_results" in st.session_state:
    results = st.session_state["weather_results"]

    city_name = results["city_name"]
    country_code = results["country_code"]
    country = results["country"]
    df = results["df"]
    compare_cities = results["compare_cities"]
    compare_years = results["compare_years"]
    city2 = results["city2"]
    year = results["year"]
    year2 = results["year2"]
    search_type = results["search_type"]
    month = results["month"]
    start_date = results["start_date"]
    end_date = results["end_date"]
    city_name2 = results["city_name2"]
    country_code2 = results["country_code2"]
    country2 = results["country2"]
    df2 = results["df2"]
    df_year = results["df_year"]

    # Creo la bandiera della prima città
    flag = (
        chr(127397 + ord(country_code[0].upper()))
        + chr(127397 + ord(country_code[1].upper()))
        if len(country_code) == 2
        else "🌍"
    )
    # se la comparazione tra città è attiva
    if compare_cities:
        flag2 = (
            chr(127397 + ord(country_code2[0].upper()))
            + chr(127397 + ord(country_code2[1].upper()))
            if len(country_code2) == 2
            else "🌍"
        )

        st.title(f"{flag} {city_name} vs {flag2} {city_name2}")
    else:
        st.title(f"{flag} {city_name}")

    # Visualizzazione delle fotografie
    if compare_cities:
        col1, col2 = st.columns(2)
        with col1:
            image_data = get_city_image(city_name)

            if image_data:
                st.image(
                    image_data["image_url"],
                    caption=f"Photo of {city_name}",
                    use_container_width=True
                )

                st.markdown(
                    f"Photo by [{image_data['photographer']}]"
                    f"({image_data['photographer_url']}) "
                    f"on [Unsplash]({image_data['photo_url']})"
                )

        with col2:
            image_data2 = get_city_image(city_name2)

            if image_data2:
                st.image(
                    image_data2["image_url"],
                    caption=f"Photo of {city_name2}",
                    use_container_width=True
                )

                st.markdown(
                    f"Photo by [{image_data2['photographer']}]"
                    f"({image_data2['photographer_url']}) "
                    f"on [Unsplash]({image_data2['photo_url']})"
                )

    else:
        image_data = get_city_image(city_name)

        if image_data:
            st.image(
                image_data["image_url"],
                caption=f"Photo of {city_name}",
                use_container_width=True
            )

            st.markdown(
                f"Photo by [{image_data['photographer']}]"
                f"({image_data['photographer_url']}) "
                f"on [Unsplash]({image_data['photo_url']})"
            )

    # Analisi dati
    st.success(f"Weather data retrieved for {city_name}")

    st.header(f"Weather report: {city_name}")

    # Opzione: KPI climatici
    st.subheader("Climate indicators")

    average_temperature = df["temperature_2m_mean"].mean()
    maximum_temperature = df["temperature_2m_max"].max()
    minimum_temperature = df["temperature_2m_min"].min()
    total_precipitation = df["precipitation_sum"].sum()
    average_humidity = df["relative_humidity_2m_mean"].mean()
    average_wind = df["wind_speed_10m_mean"].mean()
    average_sunshine = df["sunshine_duration"].mean() / 3600

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average temperature",
        f"{average_temperature:.1f} °C"
    )

    col2.metric(
        "Maximum temperature",
        f"{maximum_temperature:.1f} °C"
    )

    col3.metric(
        "Minimum temperature",
        f"{minimum_temperature:.1f} °C"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total precipitation",
        f"{total_precipitation:.1f} mm"
    )

    col2.metric(
        "Average humidity",
        f"{average_humidity:.1f} %"
    )

    col3.metric(
        "Average wind speed",
        f"{average_wind:.1f} km/h"
    )

    st.metric(
        "Average daily sunshine",
        f"{average_sunshine:.1f} hours"
    )

    # Opzione: grafico delle temperature mensili
    st.header("Monthly temperature analysis")

    monthly_temperature = (
        df.set_index("time")["temperature_2m_mean"]
        .resample("ME")
        .mean()
    )

    monthly_temperature.index = monthly_temperature.index.strftime("%B")

    st.line_chart(monthly_temperature)

    # Opzione: confronto tra le due città
    if compare_cities:

        st.header("City comparison")

        # Calcolo degli indicatori per la seconda città
        avg_temp2 = df2["temperature_2m_mean"].mean()
        max_temp2 = df2["temperature_2m_max"].max()
        min_temp2 = df2["temperature_2m_min"].min()
        precipitation2 = df2["precipitation_sum"].sum()
        wind2 = df2["wind_speed_10m_mean"].mean()

        comparison_metrics = [
            ("Average temperature", average_temperature, avg_temp2, "°C"),
            ("Maximum temperature", maximum_temperature, max_temp2, "°C"),
            ("Minimum temperature", minimum_temperature, min_temp2, "°C"),
            ("Total precipitation", total_precipitation, precipitation2, "mm"),
            ("Average wind speed", average_wind, wind2, "km/h")
        ]

        for label, value1, value2, unit in comparison_metrics:

            st.subheader(label)

            col1, col2 = st.columns(2)

            col1.metric(
                city_name,
                f"{value1:.1f} {unit}"
            )

            col2.metric(
                city_name2,
                f"{value2:.1f} {unit}",
                delta=f"{value2 - value1:+.1f} {unit}"
            )

        # Creo un DataFrame con le temperature delle due città
        comparison = pd.concat(
            [
                df.set_index("time")["temperature_2m_mean"],
                df2.set_index("time")["temperature_2m_mean"]
            ],
            axis=1
        )

        comparison.columns = [city_name, city_name2]

        # Grafico comparativo
        st.subheader("Average temperature comparison")

        st.line_chart(comparison)

        # Grafico comparativo delle precipitazioni
        st.subheader("Precipitation comparison")

        precipitation_comparison = pd.DataFrame(
            {
                city_name: [total_precipitation],
                city_name2: [precipitation2]
            },
            index=["Total precipitation"]
        )

        st.bar_chart(precipitation_comparison.T)

    # Opzione: confronto tra anni diversi
    if compare_years:

        st.header("Year comparison")

        avg_current = df["temperature_2m_mean"].mean()
        avg_previous = df_year["temperature_2m_mean"].mean()

        col1, col2 = st.columns(2)

        col1.metric(
            f"Average temperature {int(year)}",
            f"{avg_current:.1f} °C"
        )

        col2.metric(
            f"Average temperature {int(year2)}",
            f"{avg_previous:.1f} °C",
            delta=f"{avg_previous - avg_current:+.1f} °C"
        )

        # Raggruppo i dati per mese, così confronto gennaio con gennaio, febbraio con febbraio e così via
        year_comparison = pd.DataFrame({
            str(int(year)): (
                df.groupby(df["time"].dt.month)["temperature_2m_mean"].mean()
            ),
            str(int(year2)): (
                df_year.groupby(df_year["time"].dt.month)["temperature_2m_mean"].mean()
            )
        })

        year_comparison.index = [
            date(2000, int(m), 1).strftime("%B")
            for m in year_comparison.index
        ]

        st.subheader("Monthly temperature comparison")

        st.line_chart(year_comparison)

    # Grafici
    st.subheader("Temperature trends")

    fig, ax = plt.subplots(figsize=(12, 5)) # creo la finestra della figura

    ax.plot( # grafico lineare x: date, y: T medie
        df["time"],
        df["temperature_2m_mean"],
        label="Average temperature"
    )

    ax.plot( # aggiungo T max
        df["time"],
        df["temperature_2m_max"],
        label="Maximum temperature",
        alpha=0.6
    )

    ax.plot( # aggiungo T min
        df["time"],
        df["temperature_2m_min"],
        label="Minimum temperature",
        alpha=0.6
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    ax.grid(True, alpha=0.3)

    st.pyplot(fig) # visualizzo il grafico su streamlit
    plt.close(fig) # chiudo la fig matplotlib

    st.subheader("Precipitation")

    st.bar_chart( # grafico a barre
        df.set_index("time")["precipitation_sum"]
    )

    st.subheader("Wind speed")

    st.line_chart( # grafico a linee
        df.set_index("time")["wind_speed_10m_mean"]
    )

    # tabella completa
    st.subheader("Complete weather dataset")

    st.dataframe(df, use_container_width=True) # tabella interattiva. use_container... permette alla tabella di occupare tutta la larghezza disponibile

    # Esportazione dati csv
    csv = df.to_csv(index=False).encode("utf-8") # to_csv(): converte il dataframe in csv, index = false: evita di esportare l'indice della tabella, encode("utf-8"): converte il contenuto in byte, adatti al download

    st.download_button( # creo il pulsante per scaricare i dati
        "Download CSV",
        data=csv,
        file_name=f"{city_name}_weather.csv",
        mime="text/csv"
    )

    # Visualizzazione e download dei dati della seconda città
    if compare_cities:

        st.header(f"Weather report: {city_name2}")

        st.subheader("Complete weather dataset")

        st.dataframe(df2, use_container_width=True)

        csv2 = df2.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download CSV - " + city_name2,
            data=csv2,
            file_name=f"{city_name2}_weather.csv",
            mime="text/csv"
        )

    # Opzione: generazione report PDF
    st.header("Download weather report")

    pdf_buffer = BytesIO()

    pdf = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            f"Weather report: {city_name}",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            f"Period: {start_date} - {end_date}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    report_data = [
        ["Indicator", "Value"],
        ["Average temperature", f"{average_temperature:.1f} °C"],
        ["Maximum temperature", f"{maximum_temperature:.1f} °C"],
        ["Minimum temperature", f"{minimum_temperature:.1f} °C"],
        ["Total precipitation", f"{total_precipitation:.1f} mm"],
        ["Average humidity", f"{average_humidity:.1f} %"],
        ["Average wind speed", f"{average_wind:.1f} km/h"],
        ["Average daily sunshine", f"{average_sunshine:.1f} hours"]
    ]

    report_table = Table(report_data)

    report_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 8)
        ])
    )

    elements.append(report_table)

    # Se confronto due città, aggiungo anche i dati della seconda
    if compare_cities:

        elements.append(Spacer(1, 20))

        elements.append(
            Paragraph(
                f"Weather report: {city_name2}",
                styles["Heading2"]
            )
        )

        report_data2 = [
            ["Indicator", "Value"],
            ["Average temperature", f"{avg_temp2:.1f} °C"],
            ["Maximum temperature", f"{max_temp2:.1f} °C"],
            ["Minimum temperature", f"{min_temp2:.1f} °C"],
            ["Total precipitation", f"{precipitation2:.1f} mm"],
            ["Average wind speed", f"{wind2:.1f} km/h"]
        ]

        report_table2 = Table(report_data2)

        report_table2.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 8)
            ])
        )

        elements.append(report_table2)

    pdf.build(elements)

    st.download_button(
        "Download PDF report",
        data=pdf_buffer.getvalue(),
        file_name=f"{city_name}_weather_report.pdf",
        mime="application/pdf"
    )

    # Sesta funzionalità: mappa interattiva
    st.header("City location")

    latitude, longitude, _, _, _ = get_coordinates(city)

    weather_map = folium.Map(
        location=[latitude, longitude],
        zoom_start=5 if compare_cities else 10
    )

    folium.Marker(
        [latitude, longitude],
        tooltip=city_name,
        popup=f"{city_name}, {country}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(weather_map)

    if compare_cities:

        latitude2, longitude2, _, _, _ = get_coordinates(city2)

        folium.Marker(
            [latitude2, longitude2],
            tooltip=city_name2,
            popup=f"{city_name2}, {country2}",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(weather_map)

        weather_map.fit_bounds(
            [
                [latitude, longitude],
                [latitude2, longitude2]
            ]
        )

    st_folium(
        weather_map,
        width=None,
        height=450
    )
