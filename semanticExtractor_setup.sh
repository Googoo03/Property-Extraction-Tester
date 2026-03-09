#!/bin/bash

#setup virtual environment
python3 -m venv ENV
source ENV/bin/activate

#install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

for file in dataset/python_programs/*.py; do
    filename=${file##*/}

    if [ -f "tests/test_$filename" ]; then
        echo "Skipping " "$filename"
        continue
    fi

    python3 semanticExtractor.py --testFile "$filename"
done

#for file in dataset/python_programs/*.py; do
#    filename=$(basename -- "$file")
#    python3 semanticExtractor.py --testFile "$filename"
#done

#run all tests
python -m pytest tests/