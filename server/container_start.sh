#!/bin/bash
echo "Running migrations"
exec flask db upgrade
if [ "$FLASK_ENV" = "DEVELOPMENT" ]; then
    echo "Running in development mode"
    exec flask run --reload
elif [ "$FLASK_ENV" = "PRODUCTION" ]; then
    echo "Running in production mode"
    exec gunicorn -b 0.0.0.0:5000 "app.create_app:create_app(mode='production')"
fi