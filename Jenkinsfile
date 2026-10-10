pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'anilnodagala/cloudops-app'
        OPENSHIFT_API = 'https://api.rm3.7wse.p1.openshiftapps.com:6443'
        OPENSHIFT_NAMESPACE = 'crt-2832686-dev'
        OPENSHIFT_ROUTE = 'https://cloudops-route-crt-2832686-dev.apps.rm3.7wse.p1.openshiftapps.com'
    }

    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
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
            steps {
                sh '''
                    .jenkins-venv/bin/python -m pytest -v
                '''
            }
        }

        stage('Build image') {
            steps {
                sh '''
                    docker build \
                      -f openshift/Dockerfile \
                      -t ${DOCKER_IMAGE}:${BUILD_NUMBER} .
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
                        set +x

                        echo "$DOCKERHUB_TOKEN" | docker login \
                          -u "$DOCKERHUB_USER" \
                          --password-stdin

                        docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to OpenShift') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'openshift-sa-token',
                        variable: 'OPENSHIFT_TOKEN'
                    )
                ]) {
                    dir('ansible') {
                        sh '''
                            set +x

                            ansible-playbook \
                              -i inventory/hosts \
                              openshift-site.yml \
                              -e "docker_image=${DOCKER_IMAGE}:${BUILD_NUMBER}" \
                              -e "ansible_python_interpreter=/opt/ansible-venv/bin/python"
                        '''
                    }
                }
            }
        }

        stage('Verify OpenShift Deployment') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'openshift-sa-token',
                        variable: 'OPENSHIFT_TOKEN'
                    )
                ]) {
                    sh '''
                        set +x

                        /opt/ansible-venv/bin/python - <<'PY'
import os
import time
from kubernetes import client
from kubernetes.client.exceptions import ApiException

config = client.Configuration()
config.host = os.environ["OPENSHIFT_API"]
config.api_key = {
    "authorization": "Bearer " + os.environ["OPENSHIFT_TOKEN"]
}
config.verify_ssl = True

api = client.AppsV1Api(client.ApiClient(config))
namespace = os.environ["OPENSHIFT_NAMESPACE"]
expected_image = (
    os.environ["DOCKER_IMAGE"] + ":" +
    os.environ["BUILD_NUMBER"]
)

deadline = time.monotonic() + 180

while time.monotonic() < deadline:
    deployment = api.read_namespaced_deployment(
        name="cloudops-app",
        namespace=namespace
    )

    desired = deployment.spec.replicas or 1
    status = deployment.status

    image = deployment.spec.template.spec.containers[0].image
    updated = status.updated_replicas or 0
    ready = status.ready_replicas or 0
    available = status.available_replicas or 0
    observed = status.observed_generation or 0
    generation = deployment.metadata.generation or 0

    print(
        f"Image={image}, Updated={updated}/{desired}, "
        f"Ready={ready}/{desired}, "
        f"Available={available}/{desired}",
        flush=True
    )

    if (
        image == expected_image
        and observed >= generation
        and updated == desired
        and ready == desired
        and available == desired
    ):
        print("OpenShift rollout successful!")
        break

    time.sleep(5)
else:
    raise SystemExit("OpenShift rollout verification timed out")
PY
                    '''
                }
            }
        }

        stage('Verify OpenShift Route') {
            steps {
                sh '''
                    curl --fail --show-error --silent \
                      --retry 12 \
                      --retry-delay 5 \
                      --retry-all-errors \
                      "${OPENSHIFT_ROUTE}/health"
                '''
            }
        }
    }

    post {
        success {
            echo 'CloudOps OpenShift CI/CD pipeline passed!'
        }

        failure {
            echo 'CloudOps OpenShift CI/CD pipeline failed!'
        }

        always {
            sh 'rm -rf .jenkins-venv'
        }
    }
}
