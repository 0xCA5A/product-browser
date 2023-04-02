run:
	pipenv run python3.10 app.py
run_hal:
	pipenv run python3.10 app_hal.py
docker_build:
	docker build -t productmonitor .
docker_run:
	docker run --name productmonitor -d -p 5000:5000 productmonitor
