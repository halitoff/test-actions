# Time Server API

Простое FastAPI приложение для получения текущего времени сервера.

## Возможности

- Получение текущего времени в различных форматах
- Проверка состояния сервера
- Настраиваемые параметры через переменные окружения

## Установка и запуск

### Локальная установка

#### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

#### 2. Настройка переменных окружения

Скопируйте `env.example` в `.env` и настройте параметры:

```bash
cp env.example .env
```

#### 3. Запуск приложения

```bash
python main.py
```

Или через uvicorn напрямую:

```bash
uvicorn main:app --reload
```

### Docker

#### 1. Сборка образа

```bash
docker build -t time-server-api .
```

#### 2. Запуск контейнера

```bash
# Запуск с настройками по умолчанию
docker run -p 8000:8000 time-server-api

# Запуск с кастомными переменными окружения
docker run -p 8000:8000 -e HOST=0.0.0.0 -e PORT=8000 -e DEBUG=False time-server-api
```

#### 3. Запуск в фоновом режиме

```bash
docker run -d -p 8000:8000 --name time-server time-server-api
```

#### 4. Остановка контейнера

```bash
docker stop time-server
docker rm time-server
```

## API Endpoints

### GET /
Корневой эндпоинт с приветствием

### GET /time
Возвращает текущее время сервера в различных форматах:
- `current_time`: ISO формат времени
- `timestamp`: Unix timestamp
- `formatted_time`: Человекочитаемый формат
- `timezone`: Часовой пояс

### GET /health
Проверка состояния сервера

## Примеры использования

```bash
# Получить текущее время
curl http://localhost:8000/time

# Проверить состояние сервера
curl http://localhost:8000/health
```

## Настройки

Все настройки можно изменить через переменные окружения в файле `.env`:

- `HOST`: Хост для запуска сервера (по умолчанию: 0.0.0.0)
- `PORT`: Порт для запуска сервера (по умолчанию: 8000)
- `DEBUG`: Режим отладки (по умолчанию: True)

## Документация API

После запуска приложения документация доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
