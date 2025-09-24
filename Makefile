start:
	python -m ironhand

prod:
	gunicorn ironhand:app --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker
