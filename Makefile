test:
	curl -X GET http://localhost:5000/todos?links=true -H "Content-Type:application/hal+json; charset=utf-8" -v  -d "{}"
run:
	pipenv run python3.10 app.py
run_hal:
	./bootstrap.sh
docker_build:
	docker build -t productmonitor .
docker_run:
	docker run --name productmonitor -d -p 5000:5000 productmonitor
