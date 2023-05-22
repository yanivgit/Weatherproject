pipeline{
    agent{
        label 'agent'
    }
    
    stages {
        stage('Clone'){
            steps{
                // Clean workspace
                deleteDir()
        
                // Clone the gitlab repo
                checkout scmGit(branches: [[name: '*/main']], extensions: 
[], userRemoteConfigs: [[credentialsId: 'test3', url: 
'http://44.213.40.16/gitlab-instance-cab3d91b/project.git']])
            }
        }
        stage('Build Docker image'){
            steps{
                sh 'docker build -t project_image .'
            }
        }
        
        
    }
}
