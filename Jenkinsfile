pipeline {
    agent none 
    stages { 
        stage('SSH Slave Test') { 
            agent { 
                ecs { 
                    cloud 'analytics-toolkit' inheritFrom 'analytics-toolkit-jnlp-slave' 
                    } 
                    } 
        steps { 
            sh 'echo hello'
            } 
        } 
    } 
}
