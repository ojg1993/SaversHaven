#!/bin/bash

python -m pip install -r ./backend/requirements.dev.txt
cd backend
flake8 .
isort .