_Для работы с переменными окружениями необходимо создать файл .env и заполнить его согласно файлу .env.example:_
```
# SECRET_KEY
SECRET_KEY=

# Database
POSTGRES_ENGINE='django.db.backends.postgresql'
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST='db'
POSTGRES_PORT=5432
POSTGRES_HOST_AUTH_METHOD=trust

# Celery
CELERY_BROKER_URL='redis://redis:6379'
CELERY_RESULT_BACKEND='redis://redis:6379'

#Token
SEND_MESSAGE_TOKEN=

```
_Для создания образа из Dockerfile и запуска контейнера запустить команду:_
```
docker-compose up --build
```
_или_
```
docker-compose up -d --build
```
_Второй вариант для запуска в фоновом режиме._