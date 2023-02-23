FROM python:3.9-slim

WORKDIR /crmm-banking-system

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python", "app.py"]