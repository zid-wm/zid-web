import java.time.*

node {
    def app
    def buildNumber = "${BUILD_YEAR,2}.${BUILD_MONTH,2}.${BUILD_DAY,2}.${env.BUILD_NUMBER}"

    stage('Checkout Code') {
        checkout scm
    }

    stage('Build Docker Image') {
        app = docker.build("nallen013/zidartcc")
    }

    stage('Push Image to Docker Hub') {
        docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
            app.push("${buildNumber}")
            app.push("latest")
        }
    }
}
