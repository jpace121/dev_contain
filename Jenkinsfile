pipeline {
    agent any
    environment {
        BASE_CONTAINER = "registry.jpace121.net/ci/debian:latest"
    }
    stages {
        stage('Start Container') {
            steps {
                sh 'podman run -d --rm -v $PWD:/build $BASE_CONTAINER tail -f /dev/null > container-id.txt'
            }
        }
        stage('Setup') {
            steps {
                sh 'podman exec `cat container-id.txt` ansible-playbook -vvv --tags setup -i /build/inventory.yaml /build/build.yaml'
            }
        }
        stage('Build') {
            steps {
                sh 'podman exec `cat container-id.txt` ansible-playbook -vvv --tags build -i /build/inventory.yaml /build/build.yaml'
            }
        }
    }
    post {
        always {
            sh 'podman stop `cat container-id.txt`'
            sh 'rm container-id.txt'
        }
    }
}