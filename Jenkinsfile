timestamps {
	node(){
        checkout scm
        stage("Preparation"){
            sh '''
                find .
                printenv | sort
            '''
        }
        stage('Code Repository Scanned by Aqua') {
            withCredentials([
                string(credentialsId: 'AQUA_KEY', variable: 'AQUA_KEY'), 
                string(credentialsId: 'AQUA_SECRET', variable: 'AQUA_SECRET'),
                string(credentialsId: 'GITHUB_TOKEN', variable: 'GITHUB_TOKEN')
            ]) {
                sh '''
                    export AQUA_URL=https://eu-1.supply-chain.cloud.aquasec.com  
                    export CSPM_URL=https://eu-1.api.cloudsploit.com
                    export TRIVY_RUN_AS_PLUGIN=aqua
                    export trivyVersion=0.32.0
  		    curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b . v${trivyVersion}  
		    ./trivy plugin update aqua
                    ./trivy fs --debug -o report.html --security-checks config,vuln,secret .

                '''
            }
        }
        stage('Build Docker Image') {
            // fake build by downloading an image
	    // docker pull aquasaemea/mynodejs-app:1.0
            sh '''
	        echo the image has been built !!
            '''
        }
        stage('Manifest Generation') {
            withCredentials([
                // Replace GITLAB_CREDENTIALS_ID with the id of your gitlab credentials
                string(credentialsId: 'GITHUB_TOKEN', variable: 'GITHUB_TOKEN'), 
                string(credentialsId: 'AQUA_KEY', variable: 'AQUA_KEY'), 
                string(credentialsId: 'AQUA_SECRET', variable: 'AQUA_SECRET')
            ]) {
                // Replace ARTIFACT_PATH with the path to the root folder of your project 
                // or with the name:tag the newly built image
		// --artifact-path "aquasaemea/mynodejs-app:1.0"
                
                sh '''
                    export BILLY_SERVER=https://billy.eu-1.codesec.aquasec.com
                    export AQUA_URL=https://eu-1.supply-chain.cloud.aquasec.com  
                    export CSPM_URL=https://eu-1.api.cloudsploit.com                
                    export BILLY_SERVER=https://prod-aqua-billy.codesec.aquasec.com
            	    curl -sLo install.sh download.codesec.aquasec.com/billy/install.sh
            	    curl -sLo install.sh.checksum https://github.com/argonsecurity/releases/releases/latest/download/install.sh.checksum
		    if ! cat install.sh.checksum | sha256sum ; then
			echo "install.sh checksum failed"
			exit 1
		    fi
		    BINDIR="." sh install.sh
		    rm install.sh install.sh.checksum
                    ./billy health -v \
                        --aqua-key ${AQUA_KEY} \
                        --aqua-secret ${AQUA_SECRET} \
                        --access-token ${GITHUB_TOKEN} \
                        --artifact-path ./requirements.txt

                        # The docker image name:tag of the newly built image
                        # --artifact-path "my-image-name:my-image-tag" 
                        # OR the path to the root folder of your project. I.e my-repo/my-app 
                        # --artifact-path "ARTIFACT_PATH"
                '''
            }
        }
    }
}
