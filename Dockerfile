FROM python:3.9-slim

WORKDIR /crmm-banking-system

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app

EXPOSE 5000

CMD [ "python", "app/app.py"]