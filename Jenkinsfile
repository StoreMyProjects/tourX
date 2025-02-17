def img
pipeline {
    agent any
    
    environment {
        registry = 'amrendra01/flask-app'
        registryCredential = 'docker-hub-login'
        dockerImg = ''
        }
    
    stages {
        stage('Clean workspace'){
            steps{
                cleanWs disableDeferredWipeout: true, deleteDirs: true
            }
        }
        stage('Build Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/amrendra01/tourX.git']]])
            }
        }
        stage('Sonarcloud SAST scan') {
            steps {
                script {
                    withSonarQubeEnv('SonarCloud') {
                        sh ' sonar-scanner -Dsonar.organization="storemyprojects" -Dsonar.projectKey="storemyprojects_tourx" -Dsonar.sources=. -Dsonar.host.url="https://sonarcloud.io" -Dsonar.token="$SONAR_TOKEN" '
                    }
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    img = registry + ":$BUILD_ID"
                    // img = registry
                    dockerImg = docker.build("${img}")
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
        stage('Scan Docker Image with Trivy') {
            steps {
                script {
                    sh '''
                    docker pull $dockerImg
                    trivy image --exit-code 1 --severity HIGH,CRITICAL $dockerImg || echo 'Security scan failed!'
                    '''
                }
            }
        }
        stage('Update manifest file with latest image') {
            steps {
                withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'GITHUB_TOKEN')]) {
                    sh '''
                    pwd
                    sed "s/img_tag/$BUILD_ID/g" deployment-service.yaml-tmpl > deployment-service.yaml
                    cat deployment-service.yaml
                    
                    git config --global user.name "StoreMyProjects"
                    git config --global user.email singhamrendra1999@gmail.com
                    
                    git add deployment-service.yaml
                    git commit -m "Update deployment version"
                    git push https://${GITHUB_TOKEN}@github.com/StoreMyProjects/tourX HEAD:main
                    '''
                 }
            }
        }
        stage('Deploy to Kubernetes cluster') {
            steps {
                kubernetesDeploy configs: 'deployment-service.yaml', kubeConfig: [path: ''], kubeconfigId: 'eks-kube', secretName: '', ssh: [sshCredentialsId: '*', sshServer: '']
            }
        }
    }
}
