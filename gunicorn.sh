#!/bin/sh
gunicorn -w 2 src.main:app --threads 2 -b 0.0.0.0:8000