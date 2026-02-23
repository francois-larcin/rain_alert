import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()



api_key = os.getenv("OWM_API_KEY")
account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH")
twilio_phone_number = os.getenv("TWILIO_WHATSAPP")
my_phone_number = os.getenv("MY_PHONE")

MY_LAT = 50.410480
MY_LONG = 3.893230
MY_CITY = "Frameries"
CNT = 4

weather_params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": api_key,
    "units": "metric",
    "cnt": CNT,
    "exlude": "current, minutely, daily"
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=weather_params)
response.raise_for_status()

weather_data = response.json()

#Built a weather codes list for the next 12 hours
next_12h_weather_codes = [weather_data["list"][i]["weather"][0]["id"] for i in range(CNT)]


#If any of the code is <700, there will be some kind of precipitations in the next 12h
will_rain = any(code < 700 for code in next_12h_weather_codes)

print("SID:", account_sid)
print("AUTH:", auth_token)


if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
       body="It's going to rain today. Remember to bring an ☔",
       from_=twilio_phone_number,
       to=my_phone_number,
    )
    print(message.status)

