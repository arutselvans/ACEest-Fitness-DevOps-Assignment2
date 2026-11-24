
pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run Unit Tests in Docker') {
            steps {
                sh '''
                    docker run --rm \
                        --user "$(id -u):$(id -g)" \
                        -e HOME=/tmp \
                        -e PYTHONUSERBASE=/tmp/python-user \
                        -v "$WORKSPACE:/app" \
                        -w /app \
                        python:3.9-slim \
                        sh -c 'python -m pip install --user --no-cache-dir -r requirements.txt pytest-cov && python -m pytest -v --junitxml=test-results.xml --cov=app --cov-report=xml'
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                    archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }
}

