pipeline {
  agent none
  stages {
    stage('Test') {
        agent { label 'fargate-slave'}
        steps {
            sh 'echo hello from fargate'
        }
    }
  }
}
