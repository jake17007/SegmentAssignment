FROM python:3.6.6-alpine3.6

# Copy RedisProxy files to Docker container
COPY . /app
WORKDIR /app

# Initialize arguments
ARG PROXY_PORT_

# Install required Python packages
RUN pip install -r requirements.txt

# Expose the given port for the HTTP server to run on
EXPOSE $PROXY_PORT_

# Cast ARG as ENV to be used in the CMD
ENV PROXY_PORT $PROXY_PORT_

# Start the server
WORKDIR ./src
ENTRYPOINT ["sh", "-c", "gunicorn --bind 0.0.0.0:$PROXY_PORT --threads 4 --backlog $MAX_CONNECTIONS server"]
