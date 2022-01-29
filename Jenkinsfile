import java.time.*

node {
    def app
    def isMasterBranch = env.BRANCH_NAME == "master"
    def buildId = VersionNumber projectStartDate: '', versionNumberString: '${BUILD_YEAR,2}.${BUILD_MONTH,2}.${BUILD_DAY,2}'
    if (isMasterBranch) {
        def build = "${buildId}.${env.BUILD_NUMBER}"
        def buildEnv = "prod"
    } else {
        def build = "${buildId}.${env.BUILD_NUMBER}-${env.BRANCH_NAME}"
        def buildEnv = "dev"
    }


    environment {
        ENVIRONMENT = "${buildEnv}"

        DB_CREDS = credentials("${buildEnv}-db-creds")
        DB_USER = "${DB_CREDS_USR}"
        DB_PASS = "${DB_CREDS_PSW}"

        EMAIL_CREDS = credentials("${buildEnv}-email-creds")
        EMAIL_USER = "${EMAIL_CREDS_USR}"
        EMAIL_PASS = "${EMAIL_CREDS_PSW}"

        SECRET_KEY = credentials("${buildEnv}-django-secret-key")
        API_KEY = credentials("${buildEnv}-vatusa-api-key")
        ULS_K_VALUE = credentials("${buildEnv}-vatusa-uls-k-value")
    }

    stage('Checkout Code') {
        echo "Checking out code for branch: ${env.BRANCH_NAME}"
        checkout scm
        echo "Code checkout complete."
        sh "ls -R"
    }

    stage('Build Docker Image') {
        echo "Building docker image version ${build}"
        app = docker.build("nallen013/zidartcc")
        echo "Docker container image successfully built."
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
                echo "Pipeline will push version ${build}"
                app.push("${build}")
                echo "Pushed development image to Docker Hub."
            }
        }
    }

    stage('Deploy Application (Dev)') {

    }

    if (isMasterBranch) {
        stage('Deploy Application (Production)') {
            input(message='Click "Proceed" to deploy the application to production, otherwise click "Abort".')
            sh "docker-compose -f docker-compose-prod.yml up -e BUILD_VERSION=${build}"
            step([$class: 'DockerComposeBuilder', dockerComposeFile: 'docker/docker-compose-prod.yml', option: [$class: 'StartAllServices'], useCustomDockerComposeFile: true])
            echo "Container successfully started in production!"
        }
    } else {
        stage('Deploy Application (Dev)') {
            sh "docker-compose -f docker/docker-compose-dev.yml up -e BUILD_VERSION=${build}"
            // step([$class: 'DockerComposeBuilder', dockerComposeFile: 'docker/docker-compose-dev.yml', option: [$class: 'StartAllServices'], useCustomDockerComposeFile: true])
            echo "Container successfully started in dev!"
        }
    }
}
