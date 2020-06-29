# Data Analytics Toolkit

The Data Analytics Toolkit is the user interface to access to the Data Analytics Tools.

## Local Execution

#### Create local SSL certificate

`openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`

#### Environment variables

```
FLASK_APP = DataAnalyticsToolKit
FLASK_ENV = development
FLASK_DEBUG = True
FLASK_TESTING = True
```

```
GOOGLE_CLIENT_ID = Google Authentication Key Client Id
GOOGLE_CLIENT_SECRET = Google Authentication Key Client Secret
GOOGLE_DISCOVERY_URL = Google Authentication Discovery URL
```

```
GOOGLE_APPLICATION_CREDENTIALS = Google Cloud Credentials json file path
```

```
BIG_QUERY_PROJECT = Google BigQuery Project
BIG_QUERY_DATA_SET = Google BigQuery Dataset
```

#### How to run locally

`flask run --cert=cert.pem --key=key.pem`


## How to Docker

#### Build the image from the Dockerfile
```
sudo docker image build -t data_analytics_tollkit .
```

#### Run the Docker image
```
sudo docker run \
-d -p 5000:80 \
-e FLASK_ENV=$FLASK_ENV \
-e GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID \
-e GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET \
-e FLASK_TESTING=$FLASK_TESTING \
-e GOOGLE_DISCOVERY_URL=$GOOGLE_DISCOVERY_URL \
-e FLASK_APP=$FLASK_APP \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
-e BIG_QUERY_PROJECT=$BIG_QUERY_PROJECT \
-e BIG_QUERY_DATA_SET=$BIG_QUERY_DATA_SET \
-e FLASK_APP=$FLASK_APP \
-e MYSQL_USER=$MYSQL_USER \
-e MYSQL_PASSWORD=$MYSQL_PASSWORD \
-e MYSQL_HOST=$MYSQL_HOST \
-e MYSQL_TABLE=$MYSQL_TABLE \
data_analytics_tollkit:latest
```

#### List all running images
```
sudo docker ps
```

#### Stop a running image
```
sudo docker stop [CONTAINER_ID]
```

#### Delete all the inactive/stopped images
```
sudo docker image prune
```

* All the built images, are stored in the host file system,
after several builds, it takes a considerable disc space, and
it is needed to use the prune command to delete the unused images.
