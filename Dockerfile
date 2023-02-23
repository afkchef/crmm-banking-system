FROM python:3.9-slim-buster

WORKDIR /crmm-banking-system

COPY requirements.txt .

RUN pip install -r requiements.txt

COPY . .

EXPOSE 80

CMD [ "python", "app.py" ]