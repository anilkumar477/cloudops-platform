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


        stage('Deploy to kubernetes'){
            steps{
            dir('ansible') {
                sh '''
                     export KUBECONFIG=/var/jenkins_home/kubeconfig

                ansible-playbook site.yml \
                  -e "docker_image=${DOCKER_IMAGE}:${BUILD_NUMBER}" \
                  -e "ansible_python_interpreter=/opt/ansible-venv/bin/python"
                '''
            }
            }
        }
        stage('Verify deployment'){
            steps{
                sh '''
                     export KUBECONFIG=/var/jenkins_home/kubeconfig

            kubectl rollout status \
              deployment/cloudops-app \
              --timeout=120s

            kubectl get pods \
              -l app=cloudops-app

            echo "Deployed image:"
            kubectl get deployment cloudops-app \
              -o=jsonpath='{.spec.template.spec.containers[0].image}'

            echo
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
