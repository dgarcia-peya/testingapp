pipeline {
  agent {
    node {
      label 'jenkins-slave'
    }

  }
  stages {
    stage('Test') {
      agent {
        label 'jenkins-slave'
      }
      steps {
        sh 'echo hello from fargate'
      }
    }

  }
}