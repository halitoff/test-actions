from fastapi import FastAPI, HTTPException
from datetime import datetime
import uvicorn
import os
from dotenv import load_dotenv
import pytz
from typing import Optional

# Загружаем переменные окружения
load_dotenv()

# Словарь соответствий городов и часовых поясов
TIMEZONE_MAPPING = {
    "москва": "Europe/Moscow",
    "moscow": "Europe/Moscow",
    "екатеринбург": "Asia/Yekaterinburg", 
    "yekaterinburg": "Asia/Yekaterinburg",
    "новосибирск": "Asia/Novosibirsk",
    "novosibirsk": "Asia/Novosibirsk",
    "владивосток": "Asia/Vladivostok",
    "vladivostok": "Asia/Vladivostok",
    "калининград": "Europe/Kaliningrad",
    "kaliningrad": "Europe/Kaliningrad",
    "самара": "Europe/Samara",
    "samara": "Europe/Samara",
    "омск": "Asia/Omsk",
    "omsk": "Asia/Omsk",
    "красноярск": "Asia/Krasnoyarsk",
    "krasnoyarsk": "Asia/Krasnoyarsk",
    "иркутск": "Asia/Irkutsk",
    "irkutsk": "Asia/Irkutsk",
    "якутск": "Asia/Yakutsk",
    "yakutsk": "Asia/Yakutsk",
    "магадан": "Asia/Magadan",
    "magadan": "Asia/Magadan",
    "камчатка": "Asia/Kamchatka",
    "kamchatka": "Asia/Kamchatka",
    "лондон": "Europe/London",
    "london": "Europe/London",
    "париж": "Europe/Paris",
    "paris": "Europe/Paris",
    "берлин": "Europe/Berlin",
    "berlin": "Europe/Berlin",
    "токио": "Asia/Tokyo",
    "tokyo": "Asia/Tokyo",
    "пекин": "Asia/Shanghai",
    "beijing": "Asia/Shanghai",
    "шанхай": "Asia/Shanghai",
    "shanghai": "Asia/Shanghai",
    "нью-йорк": "America/New_York",
    "new_york": "America/New_York",
    "лос-анджелес": "America/Los_Angeles",
    "los_angeles": "America/Los_Angeles",
    "сидней": "Australia/Sydney",
    "sydney": "Australia/Sydney",
    "дубай": "Asia/Dubai",
    "dubai": "Asia/Dubai"
}

app = FastAPI(
    title="Time Server API",
    description="Простое API для получения текущего времени сервера и конвертации между часовыми поясами",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Корневой эндпоинт с приветствием"""
    return {"message": "Добро пожаловать в Time Server API! Используйте /time для получения текущего времени."}

@app.get("/time")
async def get_current_time():
    """Возвращает текущее время сервера"""
    current_time = datetime.now()
    return {
        "current_time": current_time.isoformat(),
        "timestamp": current_time.timestamp(),
        "formatted_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": str(current_time.astimezone().tzinfo)
    }

@app.get("/date")
async def get_current_date():
    """Возвращает текущую дату сервера"""
    current_date = datetime.now()
    return {
        "current_date": current_date.date().isoformat(),
        "formatted_date": current_date.strftime("%Y-%m-%d"),
        "day": current_date.day,
        "month": current_date.month,
        "year": current_date.year,
        "weekday": current_date.strftime("%A"),
        "weekday_number": current_date.weekday(),
        "day_of_year": current_date.timetuple().tm_yday
    }

@app.get("/datetime")
async def get_current_datetime():
    """Возвращает полную дату и время сервера"""
    current_datetime = datetime.now()
    return {
        "datetime": current_datetime.isoformat(),
        "formatted_datetime": current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "date": current_datetime.date().isoformat(),
        "time": current_datetime.time().isoformat(),
        "timestamp": current_datetime.timestamp(),
        "timezone": str(current_datetime.astimezone().tzinfo),
        "day": current_datetime.day,
        "month": current_datetime.month,
        "year": current_datetime.year,
        "hour": current_datetime.hour,
        "minute": current_datetime.minute,
        "second": current_datetime.second,
        "microsecond": current_datetime.microsecond,
        "weekday": current_datetime.strftime("%A"),
        "weekday_number": current_datetime.weekday(),
        "day_of_year": current_datetime.timetuple().tm_yday
    }

@app.get("/convert-time")
async def convert_time(
    time: str,
    timezone: str
):
    """
    Конвертирует время из UTC в указанный часовой пояс
    
    Args:
        time: Время в формате "HH:MM" или "HH:MM:SS" (UTC)
        timezone: Название города или часового пояса (например: "екатеринбург", "moscow")
    
    Returns:
        Конвертированное время в указанном часовом поясе
    """
    try:
        # Нормализуем название часового пояса
        timezone_lower = timezone.lower().strip()
        
        # Получаем часовой пояс из словаря
        if timezone_lower in TIMEZONE_MAPPING:
            target_timezone = pytz.timezone(TIMEZONE_MAPPING[timezone_lower])
        else:
            # Пробуем использовать переданное значение как есть
            try:
                target_timezone = pytz.timezone(timezone)
            except pytz.exceptions.UnknownTimeZoneError:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Неизвестный часовой пояс: {timezone}. Доступные варианты: {', '.join(TIMEZONE_MAPPING.keys())}"
                )
        
        # Парсим время
        time_parts = time.split(":")
        if len(time_parts) < 2:
            raise HTTPException(status_code=400, detail="Неверный формат времени. Используйте HH:MM или HH:MM:SS")
        
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        second = int(time_parts[2]) if len(time_parts) > 2 else 0
        
        if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
            raise HTTPException(status_code=400, detail="Неверные значения времени")
        
        # Создаем datetime объект в UTC
        utc_now = datetime.now(pytz.UTC)
        utc_time = utc_now.replace(hour=hour, minute=minute, second=second, microsecond=0)
        
        # Конвертируем в целевой часовой пояс
        local_time = utc_time.astimezone(target_timezone)
        
        # Форматируем результат
        return {
            "input_time_utc": utc_time.strftime("%H:%M:%S"),
            "input_timezone": "UTC",
            "target_timezone": str(target_timezone),
            "converted_time": local_time.strftime("%H:%M:%S"),
            "converted_datetime": local_time.isoformat(),
            "timezone_offset": local_time.strftime("%z"),
            "city_name": timezone_lower
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Ошибка парсинга времени: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")

@app.get("/health")
async def health_check():
    """Проверка состояния сервера"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    # Получаем настройки из переменных окружения
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug
    )
