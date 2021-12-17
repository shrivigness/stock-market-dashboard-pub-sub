FROM python:3.9.7

ADD producer2.py .

COPY requirements.txt .

COPY publisher2.py .

RUN pip install -r requirements.txt 

CMD ["python3","./producer2.py"]

