pipeline {
  agent any
  stages {
    stage('copy secret file') {
        steps {
                sh "whoami"
                sh "sudo cp /root/file/.env ."
            }
    }

  }

}