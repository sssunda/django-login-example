#!/bin/bash   

echo "[INFO] Start App"

# Move to parent directory
SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $SCRIPT_DIR
cd ..

source myvenv/bin/activate

python manage.py migrate

python manage.py runserver
