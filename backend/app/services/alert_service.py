import logging

logger = logging.getLogger(__name__)

def check_cold_alert(temperature_in_celsius:float) -> bool:
    return temperature_in_celsius <= 10

def check_coldwave_alert(temperature_in_celsius:float) -> bool:
    return temperature_in_celsius <= 4

def check_savere_coldwave_alert(temperature_in_celsius:float) -> bool:
    return temperature_in_celsius <= 2

def check_heatwave_alert(temperature_in_celsius:float) -> bool:
    return temperature_in_celsius >= 40

def check_heavy_rain_alert(precipitation:float) -> bool:
    return precipitation >= 50

def check_strong_wind_alert(wind_spped:float) -> bool:
    return wind_spped >= 50

def genrate_weather_alert(weather):
    alert = []
    if weather is None:
        logger.warning("Weather data not found")
        return alert
    if check_heatwave_alert(weather.temperature_in_celsius):
        alert.append({
            "type":"HEATWAVE",
            "message":"Heatwave Alert"
        }
        )

    if check_heavy_rain_alert(weather.precip_in):
        alert.append({
            "type":"HEAVY_RAIN",
            "message":"Heavy Rain Alert"
        })

    if check_strong_wind_alert(weather.wind_kph):
        alert.append({
            "type":"STRONG_WIND",
            "message":"Strong Wind Alert"
        })

    if check_cold_alert(weather.temperature_in_celsius):
        alert.append({
            "type":"MILD COLD",
            "message":"Mild cold Alert"
        })

    if check_coldwave_alert(weather.temperature_in_celsius):
        alert.append({
            "type":"Cold Wave",
            "message":"Cold Wave Alert"
        })

    if check_savere_coldwave_alert(weather.temperature_in_celsius):
        alert.append({
            "type":"FROST RISK",
            "message":"heavy cold alert"
        })

    logger.info(f"{len(alert)} alerts genrated")

    return alert

def genrate_forecast_alert(forecast_record):
    all_alerts = []
    if not forecast_record:
        logger.warning("Forecast data not found")
        return all_alerts
    for record in forecast_record:
        daily_alert = genrate_weather_alert(record)
        if daily_alert:
            all_alerts.append({
                "date":record.date,
                "alert": daily_alert
            })

    logger.info(f"{len(all_alerts)} forecast alert days found")
    return all_alerts