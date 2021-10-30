def CONTAINER_ID = 'id of container'
pipeline {
    agent any
    environment {
        BASE_CONTAINER = "registry.jpace121.net/ci/debian:latest"
    }
    stages {
        stage('Start Container') {
            steps {
                script {
                    CONTAINER_ID = sh(
                        script: "podman run -d --rm -v $PWD:/build $BASE_CONTAINER tail -f /dev/null",
                        returnStatus: true
                        returnStdout: true
                    )
                }
                sh 'echo "Run this.... ${CONTAINER_ID}"'
            }
        }
        stage('Setup') {
            steps {
                sh 'podman exec ${CONTAINER_ID} ansible-playbook --tags setup -i /build/inventory.yaml /build/build.yaml'
            }
        }
        stage('Build') {
            steps {
                sh 'podman exec ${CONTAINER_ID} ansible-playbook --tags build -i /build/inventory.yaml /build/build.yaml'
            }
        }
    }
    post {
        always {
            sh 'podman stop ${CONTAINER_ID}'
        }
    }
}