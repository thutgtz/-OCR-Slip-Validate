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
            sh "sudo docker login -u=$DOCKER_HUB_USR -p=$DOCKER_HUB_PSW"
            sh "sudo docker-compose -f docker-compose.dev.yml push"
        }
    }
    stage('deploy'){
        steps{
            sh "SSHPASS=$SSH_PSW sshpass -e ssh -o StrictHostKeyChecking=no $SSH_USR@68.183.226.229"
            sh "sudo docker login -u=$DOCKER_HUB_USR -p=$DOCKER_HUB_PSW"
            sh "sudo mkdir -p /root/app"
            sh "sudo docker run -d -v /root/app:/app thutgtz/slip-validate:dev"
            SH "exit"
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