pipeline{
    agent{
        label 'agent'
    }
    
    environment{
	DOCKERHUB_CREDENTIALS = credentials('dockerhub')
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
                sh 'sudo docker build -t avivlevari/project_image .'
            }
        }
	stage('Test Docker image'){
	    steps{
		sh 'sudo docker stop test || true
		sh 'sudo docker rm test || true'
	        sh 'sudo docker run -d -p 5000:5000 --rm --name test project_image'
		sh 'pytest test.py'
		sh 'sudo docker stop test'		
	    }
	}

	stage('Login'){
	    steps{
		sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
	    }
	}

	stage('Push'){
	    steps{
		sh 'docker push avivlevari/project_image'
	    }
	}
        
    }

    post{
	always{
	    sh 'docker logout'	
        }

	success{
	    slackSend( channel: "#succeeded-builds", token: "on_success", color: "good",message: "Build successful!")
	}
	failure{
	    slackSend( channel: "#devops-alert", token: "on_fail", color: "danger", message: "Build Failed!")
	}
    }
}
