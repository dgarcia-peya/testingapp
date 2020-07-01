pipeline {
    agent none 
    stages { 
        stage('SSH Slave Test') { 
            agent { 
                ecs { 
                    cloud 'ecs-slaves' inheritFrom 'fargate-slaves' 
                    } 
                    } 
        steps { 
            sh 'echo hello'
            } 
        } 
    } 
}
