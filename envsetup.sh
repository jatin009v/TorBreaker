
#!/bin/bash

if [ -d "Sonic/venv" ] 
then
    echo "Python virtual environment exists." 
else
    python3 -m virtualenv Sonic/venv
fi

pwd
. Sonic/venv/bin/activate

pip3 install -r Sonic/requirements.txt
python3 Sonic/manage.py makemigrations
python3 Sonic/manage.py migrate

if [ -d "logs" ] 
then
    echo "Log folder exists." 
else
    mkdir logs
    touch logs/error.log logs/access.log
fi

sudo chmod -R 777 logs