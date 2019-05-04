#!/bin/bash
python db.py
export FLASK_APP=application.py
flask run --host=0.0.0.0 --port=5000
#python db.py
#python db.py
#python application.py


