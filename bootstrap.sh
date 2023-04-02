#!/bin/sh

export FLASK_APP=./probro/app.py

pipenv run flask --debug run -h 0.0.0.0
