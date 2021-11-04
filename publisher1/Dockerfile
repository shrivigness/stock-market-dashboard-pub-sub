FROM python:3.9.7

ADD publisher1.py .

COPY requirements.txt .

RUN pip install -r requirements.txt 

CMD ["python3","./publisher1.py"]

