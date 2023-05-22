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
                sh 'sudo docker build -t project_image .'
            }
        }
	stage('Test Docker image'){
	    steps{
		sh 'sudo docker stop test || true'
		sh 'sudo docker rm test || true'
	        sh 'sudo docker run -d -p 5000:5000 --rm --name test project_image'
		sh 'pytest test.py'
		sh 'sudo docker stop test'
		sh 'sudo docker rm test'		
	    }
	}
        
        
    }
}
