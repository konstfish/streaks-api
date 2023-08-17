FROM python:3.9
COPY . /opt
WORKDIR /opt

RUN mkdir data

RUN pip install -r requirements.txt

#ENTRYPOINT [ "python", "-u", "main.py" ]

ENTRYPOINT ["gunicorn", "-c", "gunicorn_config.py", "streaks_api:app"]