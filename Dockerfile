FROM python:3

ADD main.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

EXPOSE 8080

CMD [ "/usr/local/bin/gunicorn", "-b", "0.0.0.0:8080", "main:app" ]
