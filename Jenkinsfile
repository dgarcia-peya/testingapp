pipeline {
  agent any
  stages {
    stage('GetSCM') {
      steps {
        git(url: 'https://github.com/dgarcia-peya/testingapp', credentialsId: 'dgarcia-peya')
      }
    }

    stage('Login') {
      steps {
        sh 'aws ecr get-login --no-include-email --region us-east-2 | docker login --username AWS --password-stdin 860782241405.dkr.ecr.us-east-2.amazonaws.com'
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
        sh 'docker.image(IMAGE).push()'
      }
    }

  }
  environment {
    VERSION = "${BUILD_NUMBER}"
    PROJECT = 'data-daf-toolkit-ecr'
    IMAGE = "$PROJECT:$VERSION"
    ECRURL = 'https://860782241405.dkr.ecr.us-east-2.amazonaws.com'
    ECRCRED = 'ecr:us-east-2:diego.garcia'
  }
}