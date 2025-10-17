from fastapi import FastAPI
from datetime import datetime
import uvicorn
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

app = FastAPI(
    title="Time Server API",
    description="Простое API для получения текущего времени сервера",
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
