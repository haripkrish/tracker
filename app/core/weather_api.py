import requests
from typing import Dict, Any
from app.schemas.response import WeatherInfo
from app.core.redis_conn import redis_conn
from datetime import datetime, timedelta
from app.core.config import settings


class WeatherAPI:
    def __init__(self):
        self.api_key = settings.WEATHER_PROVIDER_API_KEY
        self.base_url = settings.WEATHER_PROVIDER_BASE_API

    def fetch_weather(self, location_name: str) -> Dict[str, Any]:
        url = f"{self.base_url}/current.json?key={self.api_key}&q={location_name}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()

    def get_weather(self, location: str) -> WeatherInfo:
        weather_info = self.get_weather_from_cache(location.strip())
        if not weather_info:
            weather_info = self.get_weather_from_provider(location.strip())
        return weather_info

    def get_weather_from_provider(self, location: str) -> WeatherInfo | None:
        weather_data = self.fetch_weather(location)
        if weather_data:
            weather_info = WeatherInfo(
                location=location,
                temperature=weather_data['current']['temp_c'],
                conditions=weather_data['current']['condition']['text'],
                last_updated_at=weather_data['current']['last_updated']
            )
            try:
                weather_info.last_updated_at = weather_info.last_updated_at
                self.push_weather_to_cache(weather_info)
                print("value set")
            except Exception as e:
                print(e)
            return weather_info

    def get_weather_from_cache(self, location) -> WeatherInfo | None:
        data = redis_conn.hgetall(location)
        if data:
            return WeatherInfo(**{key.decode(): value.decode() for key, value in data.items()})

    def push_weather_to_cache(self, weather_info: WeatherInfo) -> None:
        redis_conn.hmset(weather_info.location, weather_info.model_dump())
        expiry_time = datetime.now() + timedelta(hours=2)
        redis_conn.expireat(weather_info.location, expiry_time)


weather_api = WeatherAPI()
