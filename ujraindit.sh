#!/bin/bash
rm log/1_info.log
rm log/2_debug.log
rm log/3_warning.log
rm log/4_error.log
rm log/5_critical.log
sudo systemctl stop gunicorn
sudo systemctl stop nginx
git pull origin main
python3 manage.py collectstatic --noinput --clear
sudo systemctl start gunicorn
sudo systemctl status gunicorn
sudo nginx -t && sudo systemctl start nginx
sudo systemctl status nginx

