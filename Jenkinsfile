import java.time.*

node {
    def app
    def buildNumber = "${env.BUILD_YEAR,2}.${env.BUILD_MONTH,2}.${env.BUILD_DAY,2}.${env.BUILD_NUMBER}"

    stage('Checkout Code') {
        checkout scm
        echo "Building branch ${env.BRANCH_NAME}"
    }

    stage('Build Docker Image') {
        app = docker.build("nallen013/zidartcc")
    }

    stage('Push Image to Docker Hub') {
        docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
            if (env.BRANCH_NAME == "master") {
                app.push("${buildNumber}")
                app.push("latest")
            } else {
                app.push("${buildNumber}-${env.BRANCH_NAME}")
            }
        }
    }
}
