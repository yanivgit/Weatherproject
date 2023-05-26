pipeline{

    agent{
        label 'agent'
    }
    
    environment{ 
	DOCKERHUB_CREDENTIALS = credentials('dockerhub')
	GITLAB_IP = '44.213.40.16'
	DOCKER_IMAGE = 'avivlevari/project_image'
    }
    
    stages {
        stage('Clone'){
	    steps{
		cleanWs()

		sh 'docker context use default'
		git(
		    url:"http://$GITLAB_IP/gitlab-instance-cab3d91b/project.git",
		    credentialsId: 'test3',
		    branch: 'main'
		)
	    }

	    post{
		always{
		    script{
		        env.FAILED = "fetch"
		    }
//		    slackSend( channel: "#devops-alert", token: "slack_notify", color: "danger",message: "${custom_msg_failed("Fetch")}")
		}
	    }
        }
        stage('Build Docker image'){
            steps{
                sh 'docker build -t $DOCKER_IMAG .'
            }

	    post{
		always{
		    sh 'docker rmi $(docker images -f "dangling=true" -q) || true'
                    script{
                        env.FAILED = "Build Image"
                    }
		}

//		failure{
//                  slackSend( channel: "#devops-alert", token: "slack_notify", color: "danger",message: "${custom_msg_failed("Build Image")}")
//		}
	    }
        }
	stage('Test Docker image'){
	    steps{
		sh 'docker stop test || true'
		sh 'docker rm test || true'
	        sh 'docker run -d -p 5000:5000 --rm --name test $DOCKER_IMAGE'
		sh 'pytest tests/test.py'
		sh 'docker stop test'		
	    }

            post{
                always{
//		    slackSend( channel: "#devops-alert", token: "slack_notify", color: "danger",message: "${custom_msg_failed("Tests")}")
                    script{ 
                        env.FAILED = "Tests"
                    }
                }
            }
	}

	stage('Login'){
	    steps{
		sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
	    }

            post{
                always{
//		    slackSend( channel: "#devops-alert", token: "slack_notify", color: "danger",message: "${custom_msg_failed("Loging to dockerhub")}")
                    script{ 
                        env.FAILED = "Login to dockerhub"
                    }

                }
            }

	}

	stage('Push'){
	    steps{
		sh 'docker push $DOCKER_IMAGE'
	    }

            post{

		always{
		    sh 'docker logout'
                    script{
                        env.FAILED = "Push to dockerhub"
                    }
		}
//              failure{
//		    slackSend( channel: "#devops-alert", token: "slack_notify", color: "danger",message: "${custom_msg_failed("Push to dockerhub")}")
//              }
            }
	}

//	stage('SSH Steps Rocks!') {
//	    steps {
//		sshagent(['sshUser']) {
//		    sh '''
//			scp -o StrictHostKeyChecking=no -r /home/ubuntu/workspace/sample/docker-compose.yml /home/ubuntu/workspace/sample/nginx.conf ubuntu@172.31.87.152:/home/ubuntu/
//			ssh -o StrictHostKeyChecking=no -l ubuntu 172.31.87.152 << EOF
//			    echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin
//			    sudo docker pull $DOCKER_IMAGE
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
		sh 'scp /home/ubuntu/workspace/sample/build/nginx.conf ubuntu@172.31.87.152:/home/ubuntu/'
		sh 'docker context use remote'
		sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
		sh 'docker pull $DOCKER_IMAGE'
		sh 'docker compose -f build/docker-compose.yml down'
		sh 'docker compose -f build/docker-compose.yml up -d'
	    }
	    
	    post{
		always{
		    sh 'docker logout'
                    script{
                        env.FAILED = "Deployment"
                    }
		}
		
//		failure{
//		    slackSend( channel: "#devops-alert", token: "slack_notify", color: "danger",message: "${custom_msg_failed("Deployment")}")
//		}
	    }
	}
    }
    post{
	success{
	    node('!master'){
	        slackSend( channel: "#succeeded-builds", token: "slack_notify", color: "good",message: "${custom_msg_success()}")
            }
	}
	failure{
            node('!master'){
                slackSend( channel: "#devops-alert", token: "slack_notify", color: "danger",message: "${custom_msg_failed("${env.FAILED}")}")
            }	    
	}
    }
}   

def custom_msg_success()
{
  def PUBLIC_IP = sh ( script: 'curl http://169.254.169.254/latest/meta-data/public-ipv4', returnStdout: true)
  def JENKINS_URL= "http://$PUBLIC_IP:8080"
  def JOB_NAME = env.JOB_NAME
  def BUILD_ID= env.BUILD_ID
  def JENKINS_LOG= " SUCCESS: Job [${env.JOB_NAME}] Logs path: ${JENKINS_URL}/job/${JOB_NAME}/${BUILD_ID}/consoleText"
  return JENKINS_LOG
}

def custom_msg_failed(failed)
{
  def PUBLIC_IP = sh ( script: 'curl http://169.254.169.254/latest/meta-data/public-ipv4', returnStdout: true)
  def JENKINS_URL= "http://$PUBLIC_IP:8080"
  def JOB_NAME = env.JOB_NAME
  def BUILD_ID= env.BUILD_ID
  def JENKINS_LOG= " FAILED: $failed, Logs path: ${JENKINS_URL}/job/${JOB_NAME}/${BUILD_ID}/consoleText"
  return JENKINS_LOG
}


