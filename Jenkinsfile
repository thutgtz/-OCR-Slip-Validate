pipeline {
  agent any
  {
      DOCKER_HUB = credentials('DOCKER_HUB')
  }
  stages {
    stage('copy secret file') {
        steps {
            sh "sudo cp /root/file/.env ."
            sh "echo ${DOCKER_HUB}"
        }
    }
    // stage('build && test') {
    //     steps {
    //         sh "docker-compose -f docker-compose.dev.yml build"
    //         sh "docker-compose -f docker-compose.dev.yml up"
    //     }
    // }
    // stage('push') {
    //     steps {
    //         sh "docker login -u=$REGISTRY_AUTH_USR -p=$REGISTRY_AUTH_PSW ${env.REGISTRY_ADDRESS}"
    //         sh "docker-compose -f docker-compose.yml build"
    //         sh "docker-compose -f docker-compose.yml up"
    //     }
    // }
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