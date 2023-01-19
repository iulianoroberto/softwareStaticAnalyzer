import os
import logging

PROJECT_DIR = './project_to_analize/log4j'
GIT_COMMITS_FILE = 'commits.txt'

'''
    Choose commits for CK analysis
'''
def filter_commits_by_year():
    '''
        Open commits.txt file that contain the commits log
        of the project
    '''
    try:
        all_commits = open(f'{PROJECT_DIR}/{GIT_COMMITS_FILE}', 'r+').readlines()
    except:
        logging.exception('Problem with open file')
    '''
        Select one commit for year
        (the last commit pubblished for each year)
    '''
    selected_commits = []
    i = 0
    for commit in all_commits:
        if i != len(all_commits) - 1:
            prec = commit[:4]
            curr = all_commits[i + 1][:4]
            if prec != curr:
                selected_commits.append(commit)
            i = i + 1
        else:
            prec = all_commits[i-1][:4]
            curr = commit[:4]
            if prec != curr:
                selected_commits.append(commit)
    return selected_commits

# Git log
os.system(f"cd {PROJECT_DIR} && git log --pretty=format:'%ad,%H,%an' --date=iso | sort > {GIT_COMMITS_FILE}")
print('Log commits: ok')