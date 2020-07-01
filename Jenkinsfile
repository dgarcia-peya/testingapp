pipeline {
  agent none
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