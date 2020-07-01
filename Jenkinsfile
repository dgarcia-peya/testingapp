pipeline {
  agent none

  stages {
    stage('Test') {
        agent {
            ecs {
                label 'jenkins-slave'
                inheritFrom 'jenkins-slave'
                cpu 2048
                memory 4096
                image 'jenkins/jnlp-slave'
                logDriver 'fluentd'
                logDriverOptions([[name: 'foo', value:'bar'], [name: 'bar', value: 'foo']])
                portMappings([[containerPort: 22, hostPort: 22, protocol: 'tcp'], [containerPort: 443, hostPort: 443, protocol: 'tcp']])
            }
        }
        steps {
            sh 'echo hello'
        }
    }
  }
}
