import os
import subprocess
import re
import plotly.graph_objects as go

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOSITORY_NAME = 'Java-WebSocket'
PATH_REPOSITORY = BASE_PATH + f'/project_to_analize/{REPOSITORY_NAME}'

def filter_issuse_by_status(issues_list, status_value):
    issue_list_filtered = []
    for dictionary in issues_list:
        if dictionary["status"] == status_value:
            issue_list_filtered.append(dictionary)
    return issue_list_filtered

def filter_issuse_by_labels(issues_list, labels):
    issue_list_filtered = []
    for dictionary in issues_list:
        list_labels = dictionary["labels"]
        for label in list_labels:
            if label in labels:
                issue_list_filtered.append(dictionary)
    return issue_list_filtered

def get_issue_number(issues_list):
    lenght = len(issues_list)
    return lenght

def plot_issues_table(issue_list: list):
    '''
        issue_list è una lista di dizionari, ogni dizionario rappresenta una issue
        e le sue chiavi sono le seguenti: [id, status, title, labels, date]
    '''
    issue_list.sort(key = lambda x:x['date'])
    id_list =[]
    status_list = []
    title_list = []
    date_list = []
    lable_list = []
    for dictionary in issue_list:
        labels_string = ""
        id_list.append(dictionary["id"])
        status_list.append(dictionary["status"])
        title_list.append(dictionary["title"])
        date_list.append(dictionary["date"])
        if not len(dictionary["labels"][0]) == 0:
            lenght = len(dictionary["labels"])
            i = 1
            for label in dictionary["labels"]:
                if i < lenght:
                    labels_string = labels_string + label + ", "
                else:
                    labels_string = labels_string + label
                i += 1
        else:
            labels_string = ""
        lable_list.append(labels_string)

    fig = go.Figure(data=[go.Table(
        header=dict(values=['ID', 'Status', 'Title', 'Lables', 'Date'],
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='left'),
        cells=dict(values=[id_list, # 1st column
                        status_list, # 2nd column
                        title_list, # 3nd column
                        lable_list, # 4nd column
                        date_list], # 3nd column
                line_color='darkslategray',
                fill_color='lightcyan',
                align='left'))
    ])

    fig.update_layout(autosize=True)
    fig.show()

def get_issues():
    issue_list = []
    issue_dic = {}
    bashCommand = 'gh issue list'
    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, cwd=PATH_REPOSITORY, shell=True)
    while True:
        issue_dic = {}
        line = process.stdout.readline()
        if not line:
            break
        issue = str(line.rstrip())
        issue_details = re.split(r'\\t+', issue.rstrip('\t'))
        id = issue_details[0]
        status = issue_details[1]
        title = issue_details[2]
        labels_string = str(issue_details[3]) # Is a string
        labels = labels_string.split(', ')
        date = issue_details[4]
        issue_dic["id"] = id
        issue_dic["status"] = status
        issue_dic["title"] = title
        issue_dic["labels"] = labels
        issue_dic["date"] = date
        issue_list.append(issue_dic)
    return issue_list

def main():
    print(filter_issuse_by_status(get_issues(), status_value="OPEN"))
    #print(filter_issuse_by_labels(get_issues(), ["Bug"]))
    #print(filter_issuse_by_labels(get_issues(), ["Refactor"]))
    issue_list = filter_issuse_by_status(get_issues(), status_value="OPEN")
    plot_issues_table(issue_list)

main()
