FROM python:3.6.6-alpine3.6
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ARG PORT
ENV my_port=$PORT
EXPOSE $PORT
CMD ["sh", "-c", "python ./src/redis_proxy.py $my_port"]
