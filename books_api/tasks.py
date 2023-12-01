from time import sleep
from celery import shared_task
from .scrappers import add_requested_data, scheduled_add_data


@shared_task()
def add_data(url, duration):
    data_added_to = add_requested_data(url)
    sleep(duration)
    return data_added_to


@shared_task()
def scheduled_task():
    scheduled_add_data()
