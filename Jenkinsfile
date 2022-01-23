import java.time.*

node {
    def app
    def buildId = VersionNumber projectStartDate: '', versionNumberString: '${BUILD_YEAR,2}.${BUILD_MONTH,2}.${BUILD_DAY,2}'
    def build = "${buildId}.${env.BUILD_NUMBER}"

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
                app.push("${build}")
                app.push("latest")
            } else {
                app.push("${build}-${env.BRANCH_NAME}")
            }
        }
    }
}
