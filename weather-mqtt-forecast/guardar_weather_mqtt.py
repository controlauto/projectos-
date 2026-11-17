import pandas as pd
import paho.mqtt.client as mqtt
import json
import os
from datetime import datetime
import joblib

# Connection settings come from the environment (see .env.example). No credentials in code.
MQTT_BROKER = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "weather/forecast_home")
MQTT_USER = os.environ.get("MQTT_USER")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")
CSV_FILE = os.environ.get("CSV_FILE", "weather_data.csv")

model_1h = joblib.load("modelo_temp_plus_1h.pkl")
model_3h = joblib.load("modelo_temp_plus_3h.pkl")

FEATURES = ["temperature", "dew_point", "humidity", "wind_speed", "pressure", "uv_index", "hour", "dayofweek", "minute"]

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        attrs = payload.get("attributes", {})
        now = datetime.now()

        data = {
            "timestamp": now.isoformat(),
            "temperature": attrs.get("temperature"),
            "dew_point": attrs.get("dew_point"),
            "humidity": attrs.get("humidity"),
            "wind_speed": attrs.get("wind_speed"),
            "pressure": attrs.get("pressure"),
            "uv_index": attrs.get("uv_index"),
            "hour": now.hour,
            "dayofweek": now.weekday(),
            "minute": now.minute
        }

        df_input = pd.DataFrame([data])
        X = df_input[FEATURES]
        data["pred_temp_plus_1h"] = round(model_1h.predict(X)[0], 2)
        data["pred_temp_plus_3h"] = round(model_3h.predict(X)[0], 2)

        print("📥 Real:", data["temperature"], "🌡️ +1h:", data["pred_temp_plus_1h"], "🌡️ +3h:", data["pred_temp_plus_3h"])

        df_new = pd.DataFrame([data])
        if os.path.exists(CSV_FILE):
            df_existing = pd.read_csv(CSV_FILE)
            df = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df = df_new
        df.to_csv(CSV_FILE, index=False)

    except Exception as e:
        print("❌ Error al procesar mensaje:", e)

client = mqtt.Client()
if MQTT_USER:
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC)

print(f"🚀 Conectado al broker y escuchando el topic: {MQTT_TOPIC}")
client.loop_forever()
