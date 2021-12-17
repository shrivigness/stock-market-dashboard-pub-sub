FROM python:3.9.7

ADD main.py .

COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY ./templates ./templates

CMD ["python","./main.py"]