_Для запуска проекта необходимо клонировать репозиторий и создать и активировать виртуальное окружение:_ 
```
python3 -m venv venv
```
```
source venv/bin/activate
```
_Перейти в рабочую директорию:_
```
cd mailing_service
```
_Установить зависимости:_
```
pip install -r requirements.txt
```
_Для работы с переменными окружениями необходимо создать файл .env и заполнить его согласно файлу .env.sample:_
```
# SECRET_KEY
SECRET_KEY=

# Database
POSTGRES_ENGINE='django.db.backends.postgresql'
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST='localhost'
POSTGRES_PORT=5432

# Celery
CELERY_BROKER_URL='redis://localhost:6379'
CELERY_RESULT_BACKEND='redis://localhost:6379'

#Token
SEND_MESSAGE_TOKEN=

```
_Выполнить миграции:_
```
python3 manage.py migrate
```
_Для заполнения БД запустить команду:_

```
python3 manage.py fill
```

_Для создания администратора запустить команду:_

```
python3 manage.py createsuperuser
```

_Для запуска redis_:

```
redis-cli
```

_Для запуска celery:_

```
celery -A config worker --loglevel=info
```

_Для запуска django-celery-beat:_

```
celery -A config beat --loglevel=info
```

_Для запуска приложения:_

```
python3 manage.py runserver
```
_Для тестирования проекта запустить команду:_

```
python3 manage.py test
```

_Для запуска подсчета покрытия и вывода отчет запустить команды:_

```
coverage run manage.py test

coverage report
```
