#!/bin/bash   
echo "[INFO] Start initialize"

set 

# Move to parent directory
SCRIPT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $SCRIPT_DIR
cd ..

virtualenv --python=python3.6 myvenv

source myvenv/bin/activate

pip install django~=2.0

python manage.py migrate

echo "[INFO] App initialize success"
