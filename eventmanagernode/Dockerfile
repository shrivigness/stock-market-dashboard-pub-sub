FROM python:3.9.7

ADD eventmanagernode.py .

COPY requirements.txt .

RUN pip install -r requirements.txt 

EXPOSE 5555

CMD ["python3","./eventmanagernode.py"]

