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
                docker build -t Cloudops-app:${BUILD_NUMBER} .
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