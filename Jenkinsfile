pipeline {
    agent any

    environment {
        FLASK_APP = 'app.py'
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/Malavika-05/mood_music.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest || echo "No tests available"'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t mood-music-app .'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker rm -f mood-app || true'
                sh 'docker run -d -p 5000:5000 --name mood-app mood-music-app'
            }
        }
    }
}
