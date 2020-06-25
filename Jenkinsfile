pipeline {
  agent {
    docker {
      image 'jenkins/jnlp-slave'
    }

  }
  stages {
    stage('Build') {
      steps {
        echo 'Building'
      }
    }

    stage('Test') {
      steps {
        echo 'Test'
      }
    }

    stage('Deploy') {
      steps {
        echo 'Deploy'
      }
    }

  }
  environment {
    env = 'sta'
  }
}