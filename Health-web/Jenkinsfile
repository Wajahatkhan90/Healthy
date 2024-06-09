
pipeline {
    agent any
    stages {
        stage("Fetching code") {
            steps {
                git url: "https://github.com/Bakhtawarkhan90/Health-web.git", branch: "main"
            }
        }
        stage("Building image") {
            steps {
                sh "docker build . -t health-web"
            }
        }
        stage("Docker login") {
            steps {
                echo "Logging into Docker Hub"
                withCredentials([usernamePassword(credentialsId: "Dockerhub", passwordVariable: "dockerHubPass", usernameVariable: "dockerHubUser")]) {
                    sh "docker tag health-web ${env.dockerHubUser}/health-web:latest"
                    sh "echo \$dockerHubPass | docker login -u \$dockerHubUser --password-stdin"
                    sh "docker push ${env.dockerHubUser}/health-web:latest"
                }
            }
        }
        stage("Deploy") {
            steps {
                echo "Deploying the container"
                sh "docker-compose down && docker-compose up -d"
            }
        }
    }
}
