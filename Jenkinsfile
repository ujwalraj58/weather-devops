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
                bat 'python -m pip install selenium chromedriver-autoinstaller'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo '🧪 Running automated weather app tests...'
                bat 'python tests\\test_weather.py'
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Deploying Weather App...'
                // Simulate deployment (e.g., copying to web server or starting app)
                bat '''
                echo Starting deployment...
                if not exist "C:\\Deployments\\WeatherApp" mkdir "C:\\Deployments\\WeatherApp"
                xcopy /E /I /Y app "C:\\Deployments\\WeatherApp"
                echo ✅ Deployment complete at C:\\Deployments\\WeatherApp
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Build, Tests, and Deployment Successful!'
        }
        failure {
            echo '❌ Build or Test failed. Check console output.'
        }
    }
}
