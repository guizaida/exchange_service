init:
	docker build -t currency-exchange-api .
run:
	docker run -p 8000:8000 currency-exchange-api