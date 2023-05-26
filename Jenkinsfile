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
		sh 'pytest tests/test.py'
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

		always{
		    sh 'docker logout'
		}
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
		sh 'scp /home/ubuntu/workspace/sample/build/nginx.conf ubuntu@172.31.87.152:/home/ubuntu/'
		sh 'docker context use remote'
		sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
		sh 'docker pull avivlevari/project_image'
		sh 'docker compose -f build/docker-compose.yml down'
		sh 'docker compose -f build/docker-compose.yml up -d'
	    }
	    
	    post{
		always{
		    sh 'docker logout'
		}
	    }

	}
    }
    post{
	success{
	    node('!master'){
                def ret = sh script:'curl http://169.254.169.254/latest/meta-data/public-ipv4', returnStdout: true
	        slackSend( channel: "#succeeded-builds", token: "slack_notify", color: "good",message: "${custom_msg($ret)}")
            }
	}
    }
}   

def custom_msg(ret)
{
  def JENKINS_URL= "http://$ret:8080"
  def JOB_NAME = env.JOB_NAME
  def BUILD_ID= env.BUILD_ID
  def JENKINS_LOG= " SUCCESS: Job [${env.JOB_NAME}] Logs path: ${JENKINS_URL}/job/${JOB_NAME}/${BUILD_ID}/consoleText"
  return JENKINS_LOG
}

