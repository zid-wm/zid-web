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
        echo "<b>Checking out code for branch: ${env.BRANCH_NAME}</b>"
        checkout scm
        echo "<b>\u001b[32;1mCode checkout complete.\u001b[0m</b>"
    }

    stage('Build Docker Image') {
        echo "**Building docker image version ${build}**"
        app = docker.build("nallen013/zidartcc")
        echo "<b>\u001b[32;1mDocker container image successfully built.\u001b[0m</b>"
    }

    stage('Push Image to Docker Hub') {
        echo "<b>Pushing image to Docker hub</b>"
        docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
            if (isMasterBranch) {
                echo "<b>Pipeline will push version ${build} and tag <i>latest</i></b>"
                app.push("${build}")
                app.push("latest")
                echo "<b>\u001b[32;1mPushed production image to Docker Hub.\u001b[0m</b>"
            } else {
                echo "<b>Pipeline will push version ${build}-${env.BRANCH_NAME}</b>"
                app.push("${build}-${env.BRANCH_NAME}")
                echo "<b>\u001b[32;1mPushed development image to Docker Hub.\u001b[0m</b>"
            }
        }
    }

    if (isMasterBranch) {
        stage('Deploy Application (Production)') {
            input(message='Click "Proceed" to deploy the application to production, otherwise click "Abort".')
            sh "docker-compose -f docker/docker-compose.yml -f docker/docker-compose-prod.yml up -d"
            echo "<b>\u001b[32;1mContainer successfully started in production!\u001b[0m</b>"
        }
    } else {
        stage('Deploy Application (Dev)') {
            sh "docker-compose -f docker/docker-compose.yml -f docker/docker-compose-dev.yml up -d"
            echo "<b>\u001b[32;1mContainer successfully started in dev!\u001b[0m</b>"
        }
    }
}
