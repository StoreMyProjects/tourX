
# tourX is a python-flask webapp 
1. Frontend: Bootstrap, HTML, CSS
2. Backend: python-flask
3. Database: sqlite3

### Jenkins CI/CD pipeline ==> Checkout Code on ec2 agent -> Run SonarCloud SAST scan -> Build Docker image -> Publish to DockerHub -> Run Trivy image scan -> Deployment on K8s Cluster