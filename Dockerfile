FROM python:3.9-alpine

RUN apk update && \
    apk add --no-cache python3 py3-pip curl

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# UTC Hour
RUN echo "30 23 * * * python /app/cli.py" > /etc/crontabs/root

CMD ["crond", "-f", "-l", "2"]
