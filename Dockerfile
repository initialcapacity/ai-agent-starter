FROM python:3.13

WORKDIR /apps
COPY ./discovery ./discovery
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
ENTRYPOINT [ "sh", "-c", "gunicorn --workers 4 --timeout 0 --bind=0.0.0.0:${PORT} 'discovery.app:create_app()'" ]
