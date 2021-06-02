from celery import Celery


app = Celery('tasks', broker='pyamqp://broker:5672//',
             backend='redis://backend:6379')

# app = Celery('tasks', broker='pyamqp://guest@localhost:5672//',
#              backend='redis://localhost:6379/')

# app.conf.update(
#     task_serializer='json',
#     accept_content=['json'],  # Ignore other content
#     result_serializer='json',
#     result_expires=3600,
#     timezone='Asia/Kolkota',
#     enable_utc=True,
# )

if __name__ == '__main__':
    app.start()
