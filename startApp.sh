#!/bin/sh

gunicorn -b 0.0.0.0:80 main:app