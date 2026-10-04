pipeline {
    agent any
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
                docker build -t cloudops-app:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Deploy'){
            steps{
                sh '''
                docker rm -f cloudops-container || true

                docker run -d --name cloudops-container --network cloudops-network -p 5000:5000 cloudops-app:${BUILD_NUMBER}
                '''
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
