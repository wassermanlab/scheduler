#init dotenv
from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab
import os

#configure to load dotenv from ../.env

current_dir = os.path.dirname(os.path.realpath(__file__))
load_dotenv(os.path.join(current_dir, "../.env"), override=True)

app = Celery(
    'jobs',
    broker=os.getenv("REDIS_URL"),
    include=['jobs.tasks']
    )

app.conf.update(
    timezone='America/Vancouver',
    task_annotations={
        '*': {'rate_limit': '10/h'},  # Set rate limit to 10 tasks per minute
    },
    broker_transport_options={
        'max_connections': 20,  # Use up to 20 persistent connections
    },
    beat_schedule={
        'add-every-week': {
            'task': 'jobs.tasks.add',  # Name of the task
            'schedule': crontab(day_of_week='sunday'),  # Run every Sunday
#            'schedule': crontab(minute='*/1'),  # Run every minute
            'args': (16, 16),  # Arguments to pass to the task
        },
    }
    )

if __name__ == '__main__':
        
    app.start()
    
    
    