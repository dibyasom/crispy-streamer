from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost:5672//',
             backend='redis://localhost:6379')

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Asia/Kolkota',
    enable_utc=True,
)


@app.task
def add(x, y):
    return x+y
