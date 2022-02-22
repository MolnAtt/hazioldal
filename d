[0;1;31m●[0m gunicorn.service - gunicorn daemon
     Loaded: loaded (/etc/systemd/system/gunicorn.service; enabled; vendor preset: enabled)
     Active: [0;1;31mfailed[0m (Result: exit-code) since Tue 2022-02-22 17:18:42 UTC; 2s ago
    Process: 79421 ExecStart=/home/mattila/hazi/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/mattila/hazi/hazi.sock PROJEKT.wsgi:application [0;1;31m(code=exited, status=200/CHDIR)[0m
   Main PID: 79421 (code=exited, status=200/CHDIR)
