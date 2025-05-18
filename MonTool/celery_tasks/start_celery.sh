#!/bin/bash

watchfiles "celery -A celery_tasks.celery worker -l INFO"