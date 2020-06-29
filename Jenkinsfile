pipeline {
    agent any
    environment
    {
        VERSION="${BUILD_NUMBER}
        PROJECT='data-daf-toolkit-ecr'
        IMAGE="$PROJECT:$VERSION"
        ECRURL="https://860782241405.dkr.ecr.us-east-2.amazonaws.com"
        ECRCRED='ecr:ap-us-east-2:awscredentials'
    }
    stages{
        stage('GetSCM'){
        steps{
            git'https://github.com/pedidosya/data-analysts-toolkit.git'
        }
        }
    stages('Images Build'){
        steps{
            script{
                docker.build('$IMAGE')
            }
        }
    }
    stage('Push Image'){
        steps{
            script
            {
                docker.withRegistry(ECRURL, ECRCRED)
                {
                    docker.image(IMAGE).push()
                }
            }
        }
    }
}

post 
{
    always
    {
        // make sure that the Docker image is removed
        sh "docker rmi $IMAGE | true"
    }
}
}
