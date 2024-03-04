#!/bin/bash

python -m pip install -r requirements.dev.txt
cd backend
flake8 .
isort .