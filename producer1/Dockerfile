FROM python:3.9.7

ADD producer1.py .

COPY requirements.txt .

COPY publisher1.py .

RUN pip install -r requirements.txt 

CMD ["python3","./producer1.py"]

