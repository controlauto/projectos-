# Weather forecasting dashboard (MQTT + machine learning)

Collects local weather conditions published by Home Assistant over MQTT, predicts the temperature
**1 h and 3 h ahead** with scikit-learn models, and shows real vs. predicted values in a Streamlit dashboard.

## Components
| File | Role |
|---|---|
| `guardar_weather_mqtt.py` | MQTT subscriber: reads temperature, dew point, humidity, wind speed, pressure and UV index, adds time features, predicts +1 h / +3 h and appends to `weather_data.csv` |
| `modelo_temp_plus_1h.pkl`, `modelo_temp_plus_3h.pkl` | Trained Random Forest regressors (joblib) |
| `prediccion_temperatura_rf.ipynb`, `weather_training_notebook.ipynb` | Training / evaluation notebooks (Random Forest, decision-tree baseline) |
| `dashboard_clima_app.py` | Streamlit dashboard: real vs. predicted temperature, related variables, date filter, data table |
| `weather_data.csv` | Sample dataset (~25k readings, June 2025) |

## Run
```sh
pip install -r requirements.txt
cp .env.example .env    # fill in your broker settings; .env is git-ignored
set -a; . ./.env; set +a
python guardar_weather_mqtt.py          # ingest + predictions
streamlit run dashboard_clima_app.py    # dashboard
```
Connection settings and credentials are read from environment variables only.
