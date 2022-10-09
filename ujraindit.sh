#!/bin/bash
git pull origin main
python3 manage.py collectstatic --noinput --clear
sudo systemctl restart gunicorn
sudo systemctl status gunicorn
sudo nginx -t && sudo systemctl restart nginx
sudo systemctl status nginx

