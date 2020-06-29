pipeline {
  agent any
  stages {
    stage('GetSCM') {
      steps {
        git 'https://github.com/dgarcia-peya/testingapp'
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
    ECRCRED = 'ecr:ap-us-east-2:awscredentials'
  }
  post {
    always {
      sh "docker rmi $IMAGE | true"
    }

  }
}