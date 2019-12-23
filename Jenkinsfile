pipeline {
    agent any
    environment {
        scannerHome= '/opt/sonar-scanner/bin/sonar-scanner'
    }
    
    stages {
        stage {
            steps('clone') {
                git branch: 'kishore', url: 'https://github.com/kishore1512/Python-Sample-Application.git'
            }
        }
        stage {
            steps('SonarQube analysis') {
                def scannerHome = tool 'Sonar-Scanner';
                withSonarQubeEnv('sonar') { // If you have configured more than one global server connection, you can specify its name
                sh "${scannerHome} -Dsonar.projectKey=Python -Dsonar.sources=. -Dsonar.host.url=http://18.215.62.84:9000 -Dsonar.login=832d34ef467b163050306fa45439a1383d541ad9"
                } 
            }
        }
    }
}
