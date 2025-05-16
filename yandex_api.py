import requests
from datetime import datetime
from config import YANDEX_API_KEY

def fetch_yandex_schedule(from_city_code="c54", to_city_code="c213", date=datetime.now().strftime("%Y-%m-%d")):
    """Получаем расписание поездов между городами."""
    url = "https://api.rasp.yandex.net/v3.0/search/"
    params = {
        "apikey": YANDEX_API_KEY,
        "from": from_city_code, 
        "to": to_city_code,      
        "date": date,
        "transport_types": "train",
        "limit": 5 
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("segments", [])
    else:
        print(f"Ошибка API: {response.status_code}")
        return []

