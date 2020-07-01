pipeline {
  agent none

  stages {
    stage('Test') {
        agent {
            ecs {
                label 'jenkins-slave'
                inheritFrom 'jenkins-slave'
            }
        }
        steps {
            sh 'echo hello'
        }
    }
  }
}
