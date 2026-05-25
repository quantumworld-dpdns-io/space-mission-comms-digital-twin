FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install robotframework robotframework-requests robotframework-zaplibrary

WORKDIR /tests
COPY tests/robot/ ./robot/
COPY config/robot.conf .

CMD ["robot", "--outputdir", "/output", "./robot/"]
