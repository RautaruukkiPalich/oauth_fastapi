#!/usr/bin/env bash

alembic upgrade head
uvicorn main:app --workers 4 --host 0.0.0.0 --port 8000