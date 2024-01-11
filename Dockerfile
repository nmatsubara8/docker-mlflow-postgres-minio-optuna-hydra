# our base image
FROM python:3.9.16-buster

# install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# set the working directory in the container
WORKDIR /app

# copy the requirements file and install Python dependencies
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# set environment variables
# expose the necessary port(s)
#EXPOSE 5000

# command to run on container start
#CMD ["mlflow", "server", "--backend-store-uri", "${MLFLOW_TRACKING_URI}", "--default-artifact-root", "${MLFLOW_ARTIFACT_ROOT}", "--host","0.0.0.0"]
