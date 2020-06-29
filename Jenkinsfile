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

    stage('test') {
      steps {
        echo 'testing'
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