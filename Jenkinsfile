def img
pipeline {
    agent any
    
    environment {
        registry = 'amrendra01/flask-app'
        registryCredential = 'docker-hub-login'
        dockerImg = ''
        }
    
    stages {
        stage('Build Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/amrendra01/tourX.git']]])
            }
        }
        stage('Build Image') {
            steps {
                script {
                    // img = registry + ":${env.BUILD_ID}"
                    img = registry
                    dockerImg = docker.build("${img}")
                }
            }
        }
        stage('Test Staging') {
            steps {
                sshagent(['ubuntu']) {
                    sh "docker stop flaskapp-ci-cd"
                    sh "docker rm flaskapp-ci-cd"
                    // sh "docker run -d -p 5000:5000 --name flaskapp-ci-cd-${env.BUILD_ID} ${img}"
                    sh "docker run -d -p 5000:5000 --name flaskapp-ci-cd ${img}"
                }
            }
        }
        stage('Publish Build') {
            steps {
                script {
                    docker.withRegistry('', registryCredential) {
                        dockerImg.push()
                    }
                }
            }
        }
        stage('Deploy to Kubernetes cluster') {
            steps {
                kubernetesDeploy configs: 'deployment-service.yaml', kubeConfig: [path: ''], kubeconfigId: 'eks-kube', secretName: '', ssh: [sshCredentialsId: '*', sshServer: ''], textCredentials: [certificateAuthorityData: '', clientCertificateData: '', clientKeyData: '', serverUrl: 'https://']
            }
        }
    }
}