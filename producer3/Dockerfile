FROM python:3.9.7

ADD producer3.py .

COPY requirements.txt .

COPY publisher3.py .

RUN pip install -r requirements.txt 

CMD ["python3","./producer3.py"]

