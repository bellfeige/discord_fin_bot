FROM python:3.9

RUN apt-get update

WORKDIR /bot

COPY requirements.txt .
RUN pip3 install -r requirement.txt

COPY . .

CMD ["python3", "discord_bot.py" ]
