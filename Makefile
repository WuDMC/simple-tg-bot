install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
		
test:
	python -m pytest -v tests/test_simple_bot.py

format:
	black src
	black tests

lint:
	pylint --disable=R,C *.py

all: install test format