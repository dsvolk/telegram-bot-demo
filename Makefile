install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black *.py
	isort *.py

lint:
	pylint --disable=R,C,W1203,E1101 app

all: install