FROM python:3.9.7

ADD publisher2.py .

COPY requirements.txt .

RUN pip install -r requirements.txt 

CMD ["python3","./publisher2.py"]

