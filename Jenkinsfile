pipeline {
  agent none
  stages {
    stage('SSH Slave Test') {
      agent {
        ecs {
          inheritFrom 'fargate-slaves'
        }

      }
      steps {
        sh 'echo hello'
      }
    }

  }
}