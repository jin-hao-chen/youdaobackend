@echo off

gunicorn -w 4 -b 127.0.0.1:8080 product:app

@echo on