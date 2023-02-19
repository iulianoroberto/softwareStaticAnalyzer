import os
from bs4 import BeautifulSoup
import logging
import plotly.graph_objects as go
from filter_commits import filter_commits_by_year
import numpy as np
import matplotlib.pyplot as plt
from generate_graph import get_sum_loc, get_average_fanin
import math
import scipy
from correlation_pearson.code import CorrelationPearson

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NICAD_PATH = BASE_PATH + "/Nicad/NiCad-6.2"
SYSTEM_TO_ANALIZE = "Java-WebSocket"
PROJECT_DIR = './project_to_analize/Java-WebSocket'

'''
    Apre i risulati prodotti da Nicad e legge i dati
'''
def read_results():
    # Reading the data inside the xml file to a variable under the name data
    with open(f'{BASE_PATH}/Nicad/NiCad-6.2/systems/{SYSTEM_TO_ANALIZE}_functions-consistent-clones/{SYSTEM_TO_ANALIZE}_functions-consistent-clones-0.30.xml', 'r') as f:
        data = f.read()
    return data

def plot_clones_by_year(dic:dict):
    labels = dic.keys()
    total_clones = list(map(int,list(dic.values())))

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, total_clones, width, label='Clones')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('')
    ax.set_title('Total Clones and LOC by year')
    ax.set_xticks(x, labels)
    ax.legend()

    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed')
    ax.bar_label(rects1, padding=3)

    fig.tight_layout()

    plt.show()

def plot_clones_and_loc_by_year(dic:dict):
    '''
        dic è un dizionario, la chiave rappresenta l'anno di valutazione
        e il valore associato alla chiave il numero di cloni individuato 
        rispetto al checkout al commit selezionato di quell'anno
    '''
    labels = dic.keys()
    total_clones = list(map(int,list(dic.values())))
    total_loc = get_sum_loc()

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, total_clones, width, label='Clones')
    rects2 = ax.bar(x +  width/2, total_loc, width, label='LOC')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('')
    ax.set_title('Total Clones and LOC by year')
    ax.set_xticks(x, labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed')

    fig.tight_layout()

    plt.show()

'''
    Questo metodo ritorna il numero di cloni individuati
'''
def get_number_of_clone() -> int:
    data = read_results()
    # Passing the stored data inside the beautifulsoup parser, storing the returned object
    Bs_data = BeautifulSoup(data, "xml")
    # Get clone number from XML data
    clone_info  = Bs_data.find('cloneinfo')
    clone_number_detected = clone_info.get('npairs')
    return clone_number_detected
    
'''
    Questo metodo elimina i risultati prodotti
    da Nicad durante l'analisi
'''
def delete_result():
    os.system(f"cd {NICAD_PATH} && ./cleanall")
    #os.system(f"rm {SYSTEM_TO_ANALIZE}_functions-consistent-clones")



'''
    Questo metodo esegue l'analisi con Nicad del progetto presente nella 
    directory denominata systems
'''
def execute_analysis():
    try:
        os.system(f"cd {NICAD_PATH} && ./nicad6 functions java systems/{SYSTEM_TO_ANALIZE} rename-consistent-report")
    except:
        print("Problem with Nicad execution")

def cron_analyzing(selected_commits:list) -> dict:
    dic = {}
    for commit in selected_commits:
        commit_details = commit.split(',')
        commit_date, commit_hash, commit_author = commit_details
        commit_year = commit_date[:4]
        checkout_and_analize(commit_hash, commit_year, dic)
    return dic

def checkout_and_analize(commit_hash, commit_year, dic):
    try:
        # Execute commits checkout
        os.system(f"cd {NICAD_PATH}/systems/{SYSTEM_TO_ANALIZE} && git checkout -b analysis {commit_hash}")
        print('Checkout for commit ' + commit_hash + ' : OK')
    except:
        logging.exception('Problem with checkout')
    execute_analysis()
    dic[commit_year] = get_number_of_clone()
    delete_result()
    # Move HEAD to origin branch
    os.system(f'cd {NICAD_PATH}/systems/{SYSTEM_TO_ANALIZE} && git checkout master')
    # Remove analysis branch
    os.system(f'cd {NICAD_PATH}/systems/{SYSTEM_TO_ANALIZE} && git branch -d analysis')

def plot_scatter(dic:dict):
    varaiable_one = "Number of clones"
    variale_two = "LOC"
    # Fixing random state for reproducibility
    np.random.seed(19680801)
    N = len(dic.values())
    x = dic.values()
    y = get_sum_loc()
    colors = np.random.rand(N)
    area = (30 * np.random.rand(N))**2  # 0 to 15 point radii
    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    plt.title('Clone number and LOC value correlation')
    plt.xlabel('Number of clones')
    plt.ylabel('LOC value')
    plt.grid()
    plt.show()

def calculate_correlation(dic:dict):
    elements = []
    for element in dic.values():
        elements.append(int(element))
    x_simple = np.array(elements)
    y_simple = np.array(get_sum_loc())
    my_rho = np.corrcoef(x_simple, y_simple)
    print(my_rho)
    correlation = CorrelationPearson()
    print(correlation.result(x_simple, y_simple))


def main():
    selected_commits = filter_commits_by_year()
    dic = cron_analyzing(selected_commits)
    plot_clones_and_loc_by_year(dic)
    plot_clones_by_year(dic)
    plot_scatter(dic)
    print(dic)

    elements = []
    for element in dic.values():
        elements.append(int(element))

    x_simple = np.array(elements)
    y_simple = np.array(get_sum_loc())
    print(x_simple)
    print(y_simple)
    calculate_correlation(dic)

main()