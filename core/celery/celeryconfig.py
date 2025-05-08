"""Celery config file."""

import environ

env = environ.Env()

broker_url = env("CELERY_BROKER")
result_backend = broker_url

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]

backend_max_retries = 10
task_send_sent_event = True  # an event will be emitted when task is dispatched, flower will pick up this event
timezone = "UTC"
