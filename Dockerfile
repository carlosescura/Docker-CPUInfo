FROM python:3

ADD main.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

EXPOSE 8080
HEALTHCHECK --interval=5s --timeout=3s CMD curl --fail http://localhost:8080/healthcheck || exit 1

CMD [ "/usr/local/bin/gunicorn", "-b", "0.0.0.0:8080", "main:app" ]
