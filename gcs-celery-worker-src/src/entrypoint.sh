#!/bin/bash

exec echo "Engaging celery 🚀" && sleep 10 && celery -A gcs_util worker --loglevel=INFO
