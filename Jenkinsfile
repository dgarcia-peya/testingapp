pipeline {
  agent none
  stages {
    stage('SSH Slave Test') {
      agent {
        ecs {
          inheritFrom 'analytics-toolkit-jnlp-slave'
        }

      }
      steps {
        sh 'echo hello'
      }
    }

  }
}