import os
from filter_commits import filter_commits_by_year
import logging

SONAR_QUBE_PATH = "/home/roberto/Desktop/ProgettoEQS/sonarqube-9.8.0.63668/bin/linux-x86-64"
SONAR_SCANNER_PATH = "/home/roberto/Desktop/ProgettoEQS/sonar-scanner-4.7.0.2747-linux/bin"
PROJECT_NAME  = "Java-WebSocket"

'''
    Start SonarQube server
'''
def start_sonar_qube():
    os.system(f"cd {SONAR_QUBE_PATH} && ./sonar.sh start")

'''
    Stop SonarQube server
'''
def stop_sonar_qube():
    os.system(f"cd {SONAR_QUBE_PATH} && ./sonar.sh stop")

'''
    Execute analysis with SonarScanner
'''
def sonar_scanner_analysis():
    os.system(f"cd {SONAR_SCANNER_PATH} && ./sonar-scanner")

def cron_analysis():
    selected_commits = filter_commits_by_year()
    for commit in selected_commits:
        commit_details = commit.split(',')
        commit_date, commit_hash, commit_author = commit_details
        commit_year = commit_date[:4]
        try:
            # Execute commits checkout
            os.system(f"cd {SONAR_SCANNER_PATH}/{PROJECT_NAME} && git checkout -b analysis {commit_hash}")
            print('Checkout for commit ' + commit_hash + ' : OK')
        except:
            logging.exception('Problem with checkout')
        sonar_scanner_analysis()
        # Move HEAD to origin branch
        os.system(f'cd {SONAR_SCANNER_PATH}/{PROJECT_NAME} && git checkout master')
        # Remove analysis branch
        os.system(f'cd {SONAR_SCANNER_PATH}/{PROJECT_NAME} && git branch -d analysis')

def main():
    start_sonar_qube()
    #cron_analysis()

main()