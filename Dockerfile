FROM python:3.13

WORKDIR /apps
COPY ./discovery ./discovery
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
ENTRYPOINT [ "sh", "-c", "gunicorn -w 4 'discovery.app:create_app()' --bind=0.0.0.0:${PORT}" ]
