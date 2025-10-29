pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Pulling latest code from GitHub...'
                git branch: 'main', url: 'https://github.com/ujwalraj58/weather-devops.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install selenium chromedriver-autoinstaller'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo 'Running automated weather app tests...'
                bat 'python tests\\test_weather.py'
            }
        }

        stage('Archive Artifacts') {
            steps {
                echo 'Archiving test results...'
                archiveArtifacts artifacts: '**/*.log', fingerprint: true
            }
        }
    }

    post {
        success {
            echo 'Build and Tests Successful!'
        }
        failure {
            echo 'Build or Test failed. Check console output.'
        }
    }
}


