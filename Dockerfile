FROM python:3.8

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY ./ /

EXPOSE 5000

CMD ["gunicorn", "-k", "gevent", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]