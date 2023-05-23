pipeline{
    agent{
        label 'agent'
    }
    
    environment{
	DOCKERHUB_CREDENTIALS = credentials('dockerhub')
    }
    def remote = [:]
    remote.name = "node-1"
    remote.host = "18.207.220.81"
    remote.allowAnyHosts = true
    
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

	    post{
		failure{
                    slackSend( channel: "#devops-alert", token: "slack_notify", color: "danger", message: "Build Failed!")
	    
		}
	    }
        }
	stage('Test Docker image'){
	    steps{
		sh 'sudo docker stop test || true'
		sh 'sudo docker rm test || true'
	        sh 'sudo docker run -d -p 5000:5000 --rm --name test project_image'
		sh 'pytest test.py'
		sh 'sudo docker stop test'		
	    }

            post{
                failure{
                    slackSend( channel: "#devops-alert", token: "slack_notify", color: "danger", message: "Tests Failed!")
                 
                }
            }

	}

	stage('Login'){
	    steps{
		sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
	    }

            post{
                failure{
                    slackSend( channel: "#devops-alert", token: "slack_notify", color: "danger", message: "Login to dockerhub Failed!")
                 
                }
            }

	}

	stage('Push'){
	    steps{
		sh 'docker push avivlevari/project_image'
	    }

            post{
                failure{
                    slackSend( channel: "#devops-alert", token: "slack_notify", color: "danger", message: "Push to dockerhub Failed!")
                 
                }
            }

	}

	withCredentials([sshUserPrivateKey(credentialsId: 'sshUser', keyFileVariable: 'identity', passphraseVariable: '', usernameVariable: 'userName')]) {
        remote.user = ubuntu
        remote.identityFile = identity
        stage("SSH Steps Rocks!") {
            sshCommand remote: remote, command: 'for i in {1..5}; do echo -n \"Loop \$i \"; date ; sleep 1; done'
        }
    }
        
    }

    post{
	always{
	    sh 'docker logout'	
        }

	success{
	    slackSend( channel: "#succeeded-builds", token: "slack_notify", color: "good",message: "${custom_msg()}")
	}
    }
}

def custom_msg()
{
  def JENKINS_URL= "http://44.208.24.191:8080"
  def JOB_NAME = env.JOB_NAME
  def BUILD_ID= env.BUILD_ID
  def JENKINS_LOG= " SUCCESS: Job [${env.JOB_NAME}] Logs path: ${JENKINS_URL}/job/${JOB_NAME}/${BUILD_ID}/consoleText"
  return JENKINS_LOG
}
