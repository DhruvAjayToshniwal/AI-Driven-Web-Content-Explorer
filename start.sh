#!/bin/bash

echo "Starting the Flask web server..."
export FLASK_APP=app.py
export FLASK_ENV=development
flask run &

FLASK_PID=$!
echo "Flask Server PID: $FLASK_PID"

# Wait for the server to start up
sleep 5

# Open the default web browser to the Flask app home page
xdg-open http://127.0.0.1:5000/

wait $FLASK_PID
