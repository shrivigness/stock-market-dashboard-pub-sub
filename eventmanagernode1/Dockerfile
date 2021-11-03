FROM python:3.9.7

ADD eventmanagernode1.py .

COPY requirements.txt .

RUN pip install -r requirements.txt 

EXPOSE 4500-6000

CMD ["python3","./eventmanagernode1.py"]

