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
		cleanWs()

		sh 'docker context use default'
		git(
		    url:'http://44.213.40.16/gitlab-instance-cab3d91b/project.git',
		    credentialsId: 'test3',
		    branch: 'main'
		)
	    }

	    post{
		failure{
                    slackSend( channel: "#devops-alert", token: "slack_notify", color: "danger", message: "Clone Failed!")
		}
	    }
        }
        stage('Build Docker image'){
            steps{
                sh 'docker build -t avivlevari/project_image .'
            }

	    post{

		always{
		    sh 'docker rmi $(docker images -f "dangling=true" -q) || true'
		}

		failure{
                    slackSend( channel: "#devops-alert", token: "slack_notify", color: "danger", message: "Build Failed!")
	    
		}
	    }
        }
	stage('Test Docker image'){
	    steps{
		sh 'docker stop test || true'
		sh 'docker rm test || true'
	        sh 'docker run -d -p 5000:5000 --rm --name test avivlevari/project_image'
		sh 'pytest test.py'
		sh 'docker stop test'		
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

//	stage('SSH Steps Rocks!') {
//	    steps {
//		sshagent(['sshUser']) {
//		    sh '''
//			scp -o StrictHostKeyChecking=no -r /home/ubuntu/workspace/sample/docker-compose.yml /home/ubuntu/workspace/sample/nginx.conf ubuntu@172.31.87.152:/home/ubuntu/
//			ssh -o StrictHostKeyChecking=no -l ubuntu 172.31.87.152 << EOF
//			    echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
//			    sudo docker pull avivlevari/project_image
//			    docker compose down || true
//			    docker compose up -d
//EOF
//		    '''
//
//		}
//          }
//      }


	stage('Deployment'){
	    steps{
		sh 'docker context use remote'
		sh 'docker compose down'
		sh 'docker compose up -d'
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
  def JENKINS_URL= "http://52.91.107.96:8080"
  def JOB_NAME = env.JOB_NAME
  def BUILD_ID= env.BUILD_ID
  def JENKINS_LOG= " SUCCESS: Job [${env.JOB_NAME}] Logs path: ${JENKINS_URL}/job/${JOB_NAME}/${BUILD_ID}/consoleText"
  return JENKINS_LOG
}

