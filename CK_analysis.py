import os

CK_JAR_PATH = '/home/roberto/Desktop/ProgettoEQS/ck/target/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar'
LOG4J_PROJECT_DIR = './gmaven'
csv_class_files = []

# Git checkout and CK analysis
def checkout_and_analize(commit_hash, csv_class_files, elenco_csv, commit_year):
    # Execute commits checkout
    os.system(f"cd {LOG4J_PROJECT_DIR} && git checkout -b analysis {commit_hash}")
    print('Checkout for commit ' + commit_hash + ' : ok')
    # Execute CK analysis for new branch
    os.system('mkdir analysis')
    os.system(f'java -jar {CK_JAR_PATH} {LOG4J_PROJECT_DIR} && mv class.csv class_branch_{commit_hash}_{commit_year}.csv && mv class_branch_{commit_hash}_{commit_year}.csv analysis')
    print('CK analysis for checkout ' + commit_hash + ' : ok')
    csv_class_files.append('class_branch_' + commit_hash + '_' + commit_year + '.csv')
    elenco_csv.write(f'class_branch_{commit_hash}_{commit_year}.csv,')
    # Move HEAD to origin branch
    os.system(f'cd {LOG4J_PROJECT_DIR} && git checkout gmaven-2.x')
    # Remove analysis branch
    os.system(f'cd {LOG4J_PROJECT_DIR} && git branch -d analysis')

# Extract commit and analize
def analize(selected_commits):
    elenco_csv = open("elenco_csv.txt", "w")
    for commit in selected_commits:
        commit_details = commit.split(',')
        commit_date, commit_hash, commit_author = commit_details
        commit_year = commit_date[:4]
        checkout_and_analize(commit_hash, csv_class_files, elenco_csv, commit_year)
    elenco_csv.close()