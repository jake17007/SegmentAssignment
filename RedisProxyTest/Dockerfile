FROM python:3.6.6-alpine3.6
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT python -m pytest && python populate_for_fun.py
