# projectos-
automatization
El repositorio incluye un conjunto de scripts para recopilar y visualizar datos meteorológicos. Aunque el README apenas tiene información (automatization), se observan dos aplicaciones principales en los archivos Python:

Ingesta y almacenamiento vía MQTT
El script guardar_weather_mqtt.py se conecta a un broker MQTT, lee los mensajes del topic weather/forecast_home y usa dos modelos entrenados (modelo_temp_plus_1h.pkl, modelo_temp_plus_3h.pkl) para predecir la temperatura a 1 y 3 horas. Luego guarda todo en weather_data.csv:

Carga de modelos y definición de características

Creación del registro con la lectura de MQTT y generación de predicciones

Guardado en un CSV y bucle de escucha del broker

Dashboard web con Streamlit
dashboard_clima_app.py es una aplicación Streamlit que lee el CSV y muestra gráficas de la temperatura real y de las predicciones, además de otros valores meteorológicos:

Configuración y carga del CSV

Verificación de columnas y preparación del DataFrame

Generación de gráficos de temperatura y variables relacionadas

En conjunto, el proyecto automatiza la recolección de datos climáticos, genera predicciones de temperatura a corto plazo y presenta los resultados en un dashboard interactivo.
