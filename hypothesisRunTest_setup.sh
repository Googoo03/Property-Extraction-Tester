#!/bin/bash

#setup virtual environment
python3 -m venv ENV
source ENV/bin/activate

#install dependencies
python -m pip install --upgrade pip
pip install --upgrade -r requirements.txt

#run all tests
python -m pytest tests/ -v > hypothesisRunTest_output.txt