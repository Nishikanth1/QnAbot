.PHONY: venv
venv: setup/requirements.txt
	python3 -m venv venv 
	./venv/bin/pip install  --default-timeout=100 -r setup/requirements.txt