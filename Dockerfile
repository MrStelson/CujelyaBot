FROM python:3.11

RUN mkdir /cujelya_bot

WORKDIR /cujelya_bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x ./*.sh