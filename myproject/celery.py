import os
from celery import Celery

# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Создание экземпляра приложения Celery
app = Celery('myproject')

# Использование строки здесь означает, что рабочему не нужно сериализовать
# объект конфигурации для дочерних процессов.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загрузка модулей задач из всех зарегистрированных приложений Django
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 