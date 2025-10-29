pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                echo '📥 Pulling latest code from GitHub...'
                git branch: 'main', url: 'https://github.com/ujwalraj58/weather-devops.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo '⚙️ Installing Python dependencies...'
                bat 'python -m pip install --upgrade pip'
                bat 'pip install selenium webdriver-manager'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo '🧪 Running automated weather app tests...'
                bat 'python tests/test_weather.py'
            }
        }

        stage('Archive Artifacts') {
            steps {
                echo '📦 Archiving static files...'
                archiveArtifacts artifacts: 'app/**/*.*', fingerprint: true
            }
        }

        stage('Deploy') {
            steps {
                echo '🌐 Deploying static weather app...'
                bat 'xcopy app "C:\\inetpub\\wwwroot\\weatherapp" /E /Y'
            }
        }
    }

    post {
        success {
            echo '✅ Build & Test Successful! Deployed latest version.'
        }
        failure {
            echo '❌ Build or Test failed. Check console output.'
        }
    }
}


