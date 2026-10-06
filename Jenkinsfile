pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'anilnodagala/cloudops-app'
    }
    options {
        skipDefaultCheckout(true)
    }
    stages {
        stage('Checkout scm') {
            steps {
                checkout scm
            }
        }
        stage('Setup') {
            steps {
                sh '''
                python3 --version
                python3 -m venv .jenkins-venv
                .jenkins-venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps{
                sh '''
                    .jenkins-venv/bin/python -m pytest -v
                '''
            }
        }
        stage('Build image') {
            steps{
                sh '''
                docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Push Image') {
    steps {
        withCredentials([
            usernamePassword(
                credentialsId: 'dockerhub-credentials',
                usernameVariable: 'DOCKERHUB_USER',
                passwordVariable: 'DOCKERHUB_TOKEN'
            )
        ]) {
            sh '''
                echo "$DOCKERHUB_TOKEN" | docker login \
                    -u "$DOCKERHUB_USER" \
                    --password-stdin


                docker push \
                    ${DOCKER_IMAGE}:${BUILD_NUMBER}

                docker logout
            '''
        }
    }
}


        stage('Deploy'){
            steps{
            dir('ansible') {
                sh '''
                   ansible-playbook site.yml \
                      -e "docker_image=${DOCKER_IMAGE}:${BUILD_NUMBER}"
                '''
            }
            }
        }
        stage('Verify deployment'){
            steps{
                sh '''
                   sleep 3
                   curl -f http://cloudops-container:5000/health
                '''
            }
        }

    }

    post {
        success {
            echo 'CloudOps CI pipeline passed'
        }
        failure {
            echo 'Cloudops CI pipeline failed'
        }
        always{
            sh 'rm -rf .jenkins-venv'
        }
    }
}
