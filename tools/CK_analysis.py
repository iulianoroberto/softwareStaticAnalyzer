import os
import logging

CK_JAR_PATH = '/home/roberto/Desktop/ProgettoEQS/ck/target/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar'
PROJECT_DIR = './project_to_analize/log4j'
csv_class_files = []

'''
    Git Checkout and CK analysis
'''
def checkout_and_analize(commit_hash, csv_class_files, elenco_csv, commit_year):
    # Individue project name
    project_name = PROJECT_DIR.split("/")[2]
    try:
        # Execute commits checkout
        os.system(f"cd {PROJECT_DIR} && git checkout -b analysis {commit_hash}")
        print('Checkout for commit ' + commit_hash + ' : OK')
    except:
        logging.exception('Problem with checkout')
    # Execute CK analysis for new branch
    try:
        os.system(f'mkdir result_analysis')
    except:
        logging.exception("Impossible create directory analysis")

    os.system(f'java -jar {CK_JAR_PATH} {PROJECT_DIR} && mv class.csv class_{project_name}_{commit_year}_branch_{commit_hash}.csv && mv class_{project_name}_{commit_year}_branch_{commit_hash}.csv result_analysis')
    print('CK analysis for checkout ' + commit_hash + ' : ok')
    csv_class_files.append(f'class_{project_name}_{commit_year}_branch_{commit_hash}.csv')
    elenco_csv.write(f'class_{project_name}_{commit_year}_branch_{commit_hash}.csv' + ",")
    # Move HEAD to origin branch
    os.system(f'cd {PROJECT_DIR} && git checkout gmaven-2.x')
    # Remove analysis branch
    os.system(f'cd {PROJECT_DIR} && git branch -d analysis')
    print("*************************************************************")

'''
    Extract commit and analize
'''
def analize(selected_commits):
    try:
        elenco_csv = open("elenco_csv.txt", "w")
    except:
        logging.exception('Problem with opening of elenco_csv.txt')
    for commit in selected_commits:
        commit_details = commit.split(',')
        commit_date, commit_hash, commit_author = commit_details
        commit_year = commit_date[:4]
        checkout_and_analize(commit_hash, csv_class_files, elenco_csv, commit_year)
    elenco_csv.close()