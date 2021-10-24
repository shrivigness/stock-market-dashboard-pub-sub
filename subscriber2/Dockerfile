FROM python:3.9.7

ADD subscriber2.py .

COPY requirements.txt .

RUN pip install -r requirements.txt 

CMD ["python3","./subscriber2.py"]