#!/bin/bash
rm info.log
rm debug.log
rm warning.log
rm error.log
rm critical.log
sudo systemctl stop gunicorn
sudo systemctl stop nginx
git pull origin main
python3 manage.py collectstatic --noinput --clear
sudo systemctl start gunicorn
sudo systemctl status gunicorn
sudo nginx -t && sudo systemctl start nginx
sudo systemctl status nginx

