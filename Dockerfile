FROM python:3.10-slim

RUN apt-get update && apt-get install -y make

WORKDIR /app

COPY . /app/

RUN make install

EXPOSE 8080

CMD ["python", "simple_bot.py"]
