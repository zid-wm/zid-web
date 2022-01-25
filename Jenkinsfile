import java.time.*

node {
    def app
    def buildId = VersionNumber projectStartDate: '', versionNumberString: '${BUILD_YEAR,2}.${BUILD_MONTH,2}.${BUILD_DAY,2}'
    def build = "${buildId}.${env.BUILD_NUMBER}"
    def isMasterBranch = env.BRANCH_NAME == "master"

    environment {
        BUILD_VERSION = "${build}"

        POSTGRES_CREDS = credentials('zid-db-creds')
        POSTGRES_DB = "zidartcc"
        POSTGRES_HOST = "zid_postgres"
        POSTGRES_PORT = 5432
    }

    stage('Checkout Code') {
        echo "Checking out code for branch: ${env.BRANCH_NAME}"
        checkout scm
        echo "Code checkout complete."
    }

    stage('Build Docker Image') {
        echo "Building docker image version ${build}"
        app = docker.build("nallen013/zidartcc")
        echo "Docker container image successfully built."
        sh 'printenv'
    }

    stage('Push Image to Docker Hub') {
        echo "Pushing image to Docker hub"
        docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
            if (isMasterBranch) {
                echo "Pipeline will push version ${build} and tag latest"
                app.push("${build}")
                app.push("latest")
                echo "Pushed production image to Docker Hub."
            } else {
                echo "Pipeline will push version ${build}-${env.BRANCH_NAME}"
                app.push("${build}-${env.BRANCH_NAME}")
                echo "Pushed development image to Docker Hub."
            }
        }
    }
    withEnv(
        ['BUILD_VERSION=${build}',
         'POSTGRES_CREDS_PSW=${POSTGRES_CREDS_PSW}',
         'POSTGRES_CREDS_USR=${POSTGRES_CREDS_USR}',
         'POSTGRES_DB=${POSTGRES_DB}',
         'POSTGRES_HOST=${POSTGRES_PORT}',
         'POSTGRES_PORT=${POSTGRES_PORT}']) {
        if (isMasterBranch) {
            stage('Deploy Application (Production)') {
                input(message='Click "Proceed" to deploy the application to production, otherwise click "Abort".')
                sh "docker-compose -f docker-compose-prod.yml up -e BUILD_VERSION=${build}"
                step([$class: 'DockerComposeBuilder', dockerComposeFile: 'docker/docker-compose-prod.yml', option: [$class: 'StartAllServices'], useCustomDockerComposeFile: true])
                echo "Container successfully started in production!"
            }
        } else {
            stage('Deploy Application (Dev)') {
                step([$class: 'DockerComposeBuilder', dockerComposeFile: 'docker/docker-compose-dev.yml', option: [$class: 'StartAllServices'], useCustomDockerComposeFile: true])
                echo "Container successfully started in dev!"
            }
        }
    }
}
