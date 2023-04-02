run:
	pipenv run python3.10 probro/app.py
run_hal:
	./bootstrap.sh
docker_build:
	docker build -t probro .
docker_run:
	docker run --name probro -d -p 5000:5000 probro
test:
	curl -X GET http://localhost:5000/api/products?links=true -H "Content-Type:application/hal+json; charset=utf-8" -v  -d "{}"
