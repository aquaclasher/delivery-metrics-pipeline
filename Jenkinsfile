pipeline {
    agent any

    stages {
        stage('Source Checkout') {
            steps {
                echo '=== Stage 1: Checking out source code from SCM repository ==='
                checkout scm
            }
        }

        stage('Build / Dependency Installation') {
            steps {
                echo '=== Stage 2: Installing project dependencies ==='
                sh '''
                python3 -m venv venv || true
                if [ -d "venv" ]; then
                    . venv/bin/activate
                    pip install --no-cache-dir -r requirements.txt
                else
                    python3 -m pip install --break-system-packages --no-cache-dir -r requirements.txt || pip install -r requirements.txt
                fi
                '''
            }
        }

        stage('Automated Test / Validation') {
            steps {
                echo '=== Stage 3: Running automated validation tests ==='
                sh '''
                if [ -d "venv" ]; then
                    . venv/bin/activate
                    python -m unittest test_metrics.py
                else
                    python3 -m unittest test_metrics.py
                fi
                '''
            }
        }

        stage('Deployment Packaging') {
            steps {
                echo '=== Stage 4: Packaging source and configs into dedicated deployment directory ==='
                sh '''
                # Define dedicated deployment directory
                DEPLOY_DIR="${WORKSPACE}/deployment-package"
                mkdir -p ${DEPLOY_DIR}

                # Copy exporter source and configurations
                cp delivery_metrics.py ${DEPLOY_DIR}/
                cp requirements.txt ${DEPLOY_DIR}/
                cp prometheus.yml ${DEPLOY_DIR}/
                cp alert_rules.yml ${DEPLOY_DIR}/

                # Verify runnable deployment artifact
                echo "=== Deployment Package Artifact Contents ==="
                ls -la ${DEPLOY_DIR}
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Pipeline completed! All validation tests passed and deployment artifact is packaged.'
        }
        failure {
            echo 'FAILURE: Pipeline execution failed! Review the stage error logs above.'
        }
    }
}
