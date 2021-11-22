FROM python:3.9.7

ADD subscriber1.py .

COPY requirements.txt .

COPY ./templates ./templates

RUN pip install -r requirements.txt 

CMD ["python3","./subscriber1.py"]

