#!/bin/bash

python -m venv .venv
./.venv/bin/pip install -r requirements.txt
FLASK_RUN_HOST=0.0.0.0 FLASK_DEBUG=1 ./.venv/bin/flask run -p ${1:-8888}
