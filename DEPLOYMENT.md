# Настройка автоматического деплоя

Этот документ описывает настройку автоматического деплоя FastAPI приложения с помощью GitHub Actions.

## GitHub Actions Workflow

Workflow состоит из двух джоб:

1. **build** - сборка Docker образа и публикация в GitHub Container Registry
2. **deploy** - деплой на удаленный сервер через SSH

## Настройка секретов

Для работы workflow необходимо настроить следующие секреты в GitHub репозитории:

### Переход в настройки секретов
1. Откройте ваш репозиторий на GitHub
2. Перейдите в `Settings` → `Secrets and variables` → `Actions`
3. Нажмите `New repository secret`

### Необходимые секреты

#### HOST
- **Описание**: IP-адрес или доменное имя удаленного сервера
- **Пример**: `192.168.1.100` или `myserver.com`

#### USERNAME
- **Описание**: Имя пользователя для SSH подключения
- **Пример**: `ubuntu`, `root`, `deploy`

#### SSH_KEY
- **Описание**: Приватный SSH ключ для подключения к серверу
- **Как получить**:
  ```bash
  # Создайте SSH ключ (если еще не создан)
  ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
  
  # Скопируйте приватный ключ
  cat ~/.ssh/id_rsa
  ```
- **Важно**: Скопируйте весь ключ включая `-----BEGIN OPENSSH PRIVATE KEY-----` и `-----END OPENSSH PRIVATE KEY-----`

#### PORT (опционально)
- **Описание**: SSH порт сервера
- **По умолчанию**: `22`
- **Пример**: `2222`

## Настройка сервера

### 1. Установка Docker на сервер

```bash
# Обновляем систему
sudo apt update && sudo apt upgrade -y

# Устанавливаем Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавляем пользователя в группу docker
sudo usermod -aG docker $USER

# Перезагружаемся или выходим/входим в систему
sudo reboot
```

### 2. Настройка SSH ключей

```bash
# На сервере создаем директорию для SSH ключей
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Добавляем публичный ключ в authorized_keys
echo "your_public_key_here" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### 3. Настройка доступа к GitHub Container Registry

```bash
# Создаем Personal Access Token в GitHub
# Settings → Developer settings → Personal access tokens → Tokens (classic)
# Выберите scopes: read:packages, write:packages

# Логинимся в GitHub Container Registry
echo "your_github_token" | docker login ghcr.io -u your_username --password-stdin
```

## Триггеры workflow

Workflow запускается автоматически при:
- Push в ветки `main` или `master`
- Создании Pull Request в ветки `main` или `master`

## Процесс деплоя

### Джоба build:
1. Собирает Docker образ для платформ linux/amd64 и linux/arm64
2. Публикует образ в GitHub Container Registry
3. Использует кэширование для ускорения сборки

### Джоба deploy:
1. Подключается к серверу по SSH
2. Останавливает и удаляет старый контейнер
3. Скачивает новый образ из реестра
4. Запускает новый контейнер с настройками:
   - Порт: 8000
   - Автоперезапуск: unless-stopped
   - Переменные окружения для продакшена

## Мониторинг деплоя

После успешного деплоя приложение будет доступно по адресу:
- `http://your-server-ip:8000`
- `http://your-server-ip:8000/docs` - документация API

## Отладка

### Проверка статуса контейнера
```bash
docker ps | grep time-server
```

### Просмотр логов
```bash
docker logs time-server
```

### Ручной запуск
```bash
docker run -d --name time-server -p 8000:8000 ghcr.io/your-username/your-repo:latest
```

## Безопасность

- Используйте сильные SSH ключи
- Ограничьте доступ к серверу по IP
- Регулярно обновляйте систему и Docker
- Мониторьте логи на предмет подозрительной активности
