FROM python:3.6.6-alpine3.6
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ARG PROXY_PORT
EXPOSE $PROXY_PORT
ENV PROXY_PORT_ $PROXY_PORT
CMD ["sh", "-c", "python ./src/redis_proxy.py $REDIS_ADDRESS $CACHE_EXP_SECS $CACHE_MAX_KEYS $PROXY_PORT_"]
