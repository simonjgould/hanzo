FROM python:3.8.1

WORKDIR /srv

ADD . .

RUN pip install -r requirements.txt

ENV FLASK_APP=poll_api.py

EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]