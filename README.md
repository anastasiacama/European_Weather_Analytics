# 🌍 European Weather Analytics

An interactive data analytics application built with Python and Streamlit to explore and analyze historical weather data across European capital cities.

Users can select a European capital and a specific month or year to retrieve historical weather information, visualize climate trends, compare locations and explore meteorological indicators through interactive charts and maps.

## Features

- **Historical Weather Data:** Retrieve historical weather data for European capitals.
- **City Comparison:** Compare weather conditions between two different European capitals.
- **Year Comparison:** Analyze how weather conditions change across different years.
- **Climate KPIs:** Display key meteorological indicators, including:
  - Average temperature
  - Maximum and minimum temperature
  - Total precipitation
  - Average relative humidity
  - Average wind speed
  - Average sunshine duration
- **Interactive Charts:** Visualize temperature, precipitation and other weather indicators.
- **Interactive Map:** Explore selected cities on an interactive map.
- **PDF Report:** Generate downloadable PDF reports containing weather statistics.
- **CSV Export:** Download weather datasets for further analysis.
- **City Images:** Display city images with photographer attribution.
- **Data Caching:** Improve performance by avoiding unnecessary repeated API requests.

## Weather Indicators

The application retrieves several daily meteorological variables:

- Mean, maximum and minimum temperature (°C)
- Total precipitation (mm)
- Rainfall (mm)
- Precipitation duration (hours)
- Maximum and mean wind speed (km/h)
- Mean relative humidity (%)
- Sunshine duration
- Shortwave radiation
- Weather conditions (weather code)

## Project Structure

```text
European-Weather-Analytics/
│
├── app.py                  # Main Streamlit application
├── weather_api.py          # Weather data retrieval and processing
├── image_api.py            # City image retrieval from Unsplash
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
│
└── .streamlit/
    └── secrets.toml        # API credentials (not committed to GitHub)
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/anastasiacama/European-Weather-Analytics.git
```

### 2. Navigate to the project folder

```bash
cd European-Weather-Analytics
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API credentials

Create a `.streamlit/secrets.toml` file and add your Unsplash API key:

```toml
UNSPLASH_ACCESS_KEY = "your_unsplash_access_key"
```

The Open-Meteo API does not require an API key for the endpoints used by this project.


### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## APIs Used

### Open-Meteo

Used to retrieve:
- Geographic coordinates through the Geocoding API.
- Historical daily weather data through the Historical Weather API.

Documentation: https://open-meteo.com/

### Unsplash

Used to retrieve city images and display photographer attribution.

Documentation: https://unsplash.com/developers

## Project Goals

This project was developed to practice and demonstrate practical skills in:

- Python programming
- Data collection through REST APIs
- Data cleaning and manipulation with Pandas
- Exploratory Data Analysis (EDA)
- Data visualization
- Interactive dashboard development
- Working with external libraries and services
- Building and documenting a complete data analytics project
