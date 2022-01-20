pipeline {
  agent any
  environment {
      DOCKER_HUB = credentials('DOCKER_HUB')
      SSH = credentials('SSH')
  }
  stages {
    stage('copy secret file') {
        steps {
            sh "sudo cp /root/file/.env ."
        }
    }
    stage('build && test') {
        steps {
            sh "sudo docker-compose -f docker-compose.dev.yml build"
            sh "sudo docker-compose -f docker-compose.dev.yml up"
        }
    }
    stage('push') {
        steps {
            sh "sudo echo '$DOCKER_HUB_PSW' | docker login --username $DOCKER_HUB_USR --password-stdin"
            sh "sudo docker-compose -f docker-compose.yml build"
            sh "sudo docker-compose -f docker-compose.yml push"
        }
    }
    stage('deploy'){
        steps{
            sh "SSHPASS=$SSH_PSW sshpass -e ssh -o StrictHostKeyChecking=no $SSH_USR@68.183.226.229"
            sh "sudo echo '$DOCKER_HUB_PSW' | docker login --username $DOCKER_HUB_USR --password-stdin && \
                sudo mkdir -p /root/app  && \
                sudo docker run -d -v /root/app:/app thutgtz/slip-validate:dev && \
                exit"
        }
    }
  }
  post {
    always {
        sh "docker-compose down || true"
    }
    unsuccessful{
        sh "echo 'failedddd'"
    }
  }   

}