pipeline {
  agent {
    label 'peya-data-ecs-jenkins-slave'
  }
  stages {
    stage('GetSCM') {
      steps {
        checkout scm
      }
    }

    stage('Images Build') {
      steps {
        script {
          docker.build('$IMAGE')
        }

      }
    }

    stage('Push Image') {
      steps {
        script {
          docker.withRegistry(ECRURL, ECRCRED)
          {
            docker.image(IMAGE).push()
          }
        }

      }
    }

  }
  environment {
    VERSION = "${BUILD_NUMBER}"
    PROJECT = 'data-daf-toolkit-ecr'
    IMAGE = "$PROJECT:$VERSION"
    ECRURL = 'https://860782241405.dkr.ecr.us-east-2.amazonaws.com'
    ECRCRED = 'ecr:us-east-2:ECR'
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