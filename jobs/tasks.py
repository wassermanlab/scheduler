
from .celery import app

@app.task
def add(x, y):
    print("doing an add.")
    return x + y