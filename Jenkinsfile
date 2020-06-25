pipeline {
  agent {
    docker {
      image 'jenkins/jnlp-slave'
    }

  }
  stages {
    stage('Checkout') {
      steps {
        readTrusted 'Jenkinsfile'
      }
    }

    stage('Build') {
      parallel {
        stage('Build Images') {
          steps {
            sh 'docker image build -t data-daf-toolkit-ecr .'
          }
        }

        stage('Taging Images') {
          steps {
            sh 'docker tag  860782241405.dkr.ecr.us-east-2.amazonaws.com/data-daf-toolkit-ecr:latest'
          }
        }

        stage('Pushing Images') {
          steps {
            sh 'docker push 860782241405.dkr.ecr.us-east-2.amazonaws.com/data-daf-toolkit-ecr:latest'
          }
        }

      }
    }

    stage('Test') {
      steps {
        echo 'Test'
      }
    }

    stage('Deploy') {
      steps {
        sh '''sudo docker run \\
-d -p 5000:80 \\
-e FLASK_ENV=$FLASK_ENV \\
-e GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID \\
-e GOOGLE_CLIENT_SECRET=$GOOGLE_CLIENT_SECRET \\
-e FLASK_TESTING=$FLASK_TESTING \\
-e GOOGLE_DISCOVERY_URL=$GOOGLE_DISCOVERY_URL \\
-e FLASK_APP=$FLASK_APP \\
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \\
-e BIG_QUERY_PROJECT=$BIG_QUERY_PROJECT \\
-e BIG_QUERY_DATA_SET=$BIG_QUERY_DATA_SET \\
-e FLASK_APP=$FLASK_APP \\
-e MYSQL_USER=$MYSQL_USER \\
-e MYSQL_PASSWORD=$MYSQL_PASSWORD \\
-e MYSQL_HOST=$MYSQL_HOST \\
-e MYSQL_TABLE=$MYSQL_TABLE \\
data-daf-toolkit-ecr:latest'''
      }
    }

    stage('Post') {
      steps {
        error 'Error'
      }
    }

  }
  environment {
    env = 'sta'
    FLASK_APP = 'DataAnalyticsToolKit'
    FLASK_ENV = 'development'
    FLASK_DEBUG = 'True'
    FLASK_TESTING = 'True'
    GOOGLE_CLIENT_ID = 'Google Authentication Key Client Id'
    GOOGLE_CLIENT_SECRET = 'Google Authentication Key Client Secret'
    GOOGLE_DISCOVERY_URL = 'Google Authentication Discovery URL'
    GOOGLE_APPLICATION_CREDENTIALS = 'Google Cloud Credentials json file path'
    BIG_QUERY_PROJECT = 'Google BigQuery Project'
    BIG_QUERY_DATA_SET = 'Google BigQuery Dataset'
  }
}