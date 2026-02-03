base:
	.\ENV\Scripts\activate
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	python3 semanticExtractor.py