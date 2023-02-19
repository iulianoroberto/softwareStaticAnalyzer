import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends import _backend_tk
import matplotlib.transforms as transforms
import matplotlib.cbook as cbook
import plotly.express as px

WMC_LIMIT = 14
DIT_LIMIT = 7
NOC_LIMIT = 3
CBO_LIMIT = 2
GIT_COMMITS_FILE = 'elenco_csv.txt'
ANALISYS_DIR = 'result_analysis'

def read_class_csv():
    class_csv_file_list = []
    file = open(f'{GIT_COMMITS_FILE}', 'r+').readlines()
    for i in range(len(file[0].split(','))-1):
        class_csv_file_list.append(file[0].split(',')[i])
    return class_csv_file_list

# Metric data manipulate (sum and average of values)
def metric_value_manipulate(class_csv_file_list):
    metric_sum_dict = {}
    for file_name in class_csv_file_list:
        metrics = pd.read_csv(f'{ANALISYS_DIR}/{file_name}')
        year = file_name.split('_')[2]
        total_loc = metrics['loc'].sum()
        average_wmc = metrics['wmc'].mean()
        average_cbo = metrics['cbo'].mean()
        average_dit = metrics['dit'].mean()
        average_noc = metrics['noc'].mean()
        average_rfc = metrics['rfc'].mean()
        average_fanin = metrics['fanin'].mean()
        average_fanout = metrics['fanout'].mean()
        metric_sum_dict[year] = total_loc, average_wmc, average_cbo, average_dit, average_noc, average_rfc, average_fanin, average_fanout
    return(metric_sum_dict)

def metric_value_manipulate_for_class():
    class_csv_file_list = read_class_csv()
    dic = {}
    for file_name in class_csv_file_list:
        dataframe = pd.read_csv(f'{ANALISYS_DIR}/{file_name}')
        print("Analizzo il file: " + file_name)
        for row in dataframe.iterrows():
            if list(row[1])[2] == "class":
                key = list(row[1])[1].split('.')[-1]
                cbo = list(row[1])[3]
                fanin = list(row[1])[5]
                fanout = list(row[1])[6]
                wmc = list(row[1])[7]
                dit = list(row[1])[8]
                rfc = list(row[1])[10]
                loc = list(row[1])[34]
                rfc_limit = (wmc*dit) + 1
                if key not in dic:
                    dic[key] = [[cbo],[fanin],[fanout],[wmc],[dit],[rfc],[loc],[rfc_limit]]
                else:
                    dic.get(key)[0].append(cbo)
                    dic.get(key)[1].append(fanin)
                    dic.get(key)[2].append(fanout)
                    dic.get(key)[3].append(wmc)
                    dic.get(key)[4].append(dit)
                    dic.get(key)[5].append(rfc)
                    dic.get(key)[6].append(loc)
                    dic.get(key)[7].append(rfc_limit)

    return dic



# Plot generic bar color graph
def combine_plot_generic_bar_graph(x_data, y_data, ylabel, title, ax, x_position, y_position, limit_value):
    ax[x_position, y_position].bar(x_data, y_data)
    ax[x_position, y_position].set_ylabel(ylabel)
    ax[x_position, y_position].set_title(title)
    #ax[x_position, y_position].grid(True, linestyle='-.')
    ax[x_position, y_position].set_axisbelow(True)
    ax[x_position, y_position].yaxis.grid(color='gray', linestyle='dashed')
    ax[x_position, y_position].tick_params(labelcolor='r', labelsize='medium', width=3)
    if limit_value != 0:
        ax[x_position, y_position].axhline(y=limit_value, color='r', linestyle='-')
    return ax

# Plot generic axes pros graph
def combine_plot_generic_axes_pros_graph(x_data, y_data, ylabel, title, ax, x_position, y_position, limit_value):
    ax[x_position, y_position].plot(x_data, y_data)
    ax[x_position, y_position].grid(True, linestyle='-.')
    ax[x_position, y_position].tick_params(labelcolor='r', labelsize='medium', width=3)
    ax[x_position, y_position].set_title(title)
    ax[x_position, y_position].set_ylabel(ylabel)
    if limit_value != 0:
        ax[x_position, y_position].axhline(y=limit_value, color='r', linestyle='-')
    return ax

# Plot generic box plot graph
def plot_boxplot_graph(list, dic, title, limit_value):
    fig, ax = plt.subplots()
    bplot1 = ax.boxplot(list,
                         vert=True,  # vertical box alignment
                         patch_artist=True,  # fill with color
                         labels=dic.keys())  # will be used to label x-ticks
    ax.set_title(title)
    if limit_value != 0:
        ax.axhline(y=limit_value, color='r', linestyle='-')
    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed')
    plt.xticks(rotation=90)
    plt.tick_params(labelcolor='r', labelsize='medium', width=3)
    fig.subplots_adjust(bottom=0.4)
    figManager = plt.get_current_fig_manager()
    figManager.resize(*figManager.window.maxsize())
    plt.grid()
    plt.show()

def get_sum_loc():
    class_csv_file_list = read_class_csv()
    metric_sum_dict = metric_value_manipulate(class_csv_file_list)
    sum_loc = []
    average_of_wmc = []
    average_cbo = []
    average_dit = []
    average_noc = []
    average_rfc = []
    average_fanin = []
    average_fanout = []
    for i in metric_sum_dict.keys():
        sum_loc.append(metric_sum_dict[i][0])
        average_of_wmc.append(metric_sum_dict[i][1])
        average_cbo.append(metric_sum_dict[i][2])
        average_dit.append(metric_sum_dict[i][3])
        average_noc.append(metric_sum_dict[i][4])
        average_rfc.append(metric_sum_dict[i][5])
        average_fanin.append(metric_sum_dict[i][6])
        average_fanout.append(metric_sum_dict[i][7])
    return sum_loc

def get_average_fanin():
    class_csv_file_list = read_class_csv()
    metric_sum_dict = metric_value_manipulate(class_csv_file_list)
    average_fanin = []
    for i in metric_sum_dict.keys():
        average_fanin.append(metric_sum_dict[i][6])
    return average_fanin

def get_average_fanout():
    class_csv_file_list = read_class_csv()
    metric_sum_dict = metric_value_manipulate(class_csv_file_list)
    average_fanout = []
    for i in metric_sum_dict.keys():
        average_fanout.append(metric_sum_dict[i][7])
    return average_fanout

def plot_scatter(varaiable_one = "Fan-in", variale_two = "Fan-out"):
    # Fixing random state for reproducibility
    np.random.seed(19680801)
    N = len(get_average_fanout())
    x = get_average_fanin()
    y = get_average_fanout()
    colors = np.random.rand(N)
    area = (30 * np.random.rand(N))**2  # 0 to 15 point radii
    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    plt.title('Fan-in and Fan-out correlation')
    plt.xlabel('Fan-in')
    plt.ylabel('Fan-out')
    plt.grid()
    plt.show()

def plot_3d_scatter():
    x = get_average_fanin()
    print(x)
    y = get_average_fanout()
    print(y)
    z = get_sum_loc()

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z,
            linewidths=1, alpha=.7,
            edgecolor='k',
            s = 200,
            c=z)
    ax.set_xlabel('Fan-in')
    ax.set_ylabel('Fan-out')
    ax.set_zlabel('LOC', rotation=90)
    plt.title('Fan-in, Fan-out and LOC correlation')
    plt.show()

# Plot anlasys's graph
def plotting():
    class_csv_file_list = read_class_csv()
    metric_sum_dict = metric_value_manipulate(class_csv_file_list)

    sum_loc = []
    average_of_wmc = []
    average_cbo = []
    average_dit = []
    average_noc = []
    average_rfc = []
    average_fanin = []
    average_fanout = []
    for i in metric_sum_dict.keys():
        sum_loc.append(metric_sum_dict[i][0])
        average_of_wmc.append(metric_sum_dict[i][1])
        average_cbo.append(metric_sum_dict[i][2])
        average_dit.append(metric_sum_dict[i][3])
        average_noc.append(metric_sum_dict[i][4])
        average_rfc.append(metric_sum_dict[i][5])
        average_fanin.append(metric_sum_dict[i][6])
        average_fanout.append(metric_sum_dict[i][7])
    
    global FANIN_AVERAGE
    FANIN_AVERAGE = sum(average_fanin)/len(average_fanin)

    global FANOUT_AVERAGE
    FANOUT_AVERAGE = sum(average_fanout)/len(average_fanout)

    global LOC_AVERAGE
    LOC_AVERAGE = sum(sum_loc)/len(sum_loc)

    global DIT_AVERAGE
    DIT_AVERAGE = sum(average_dit)/len(average_dit)

    global RFC_AVERAGE
    RFC_AVERAGE = sum(average_rfc)/len(average_rfc)

    
    


    fig, ax = plt.subplots(2,2)

    combine_plot_generic_axes_pros_graph(metric_sum_dict.keys(), sum_loc, "Total LOC by year", "Total LOC", ax, 0, 0, 0)
    combine_plot_generic_axes_pros_graph(metric_sum_dict.keys(), average_of_wmc, "Average value of WMC by year (all class)", "Average value of WMC", ax, 0, 1, 14)
    combine_plot_generic_axes_pros_graph(metric_sum_dict.keys(), average_dit, "Average value of DIT by year (all class)", "Average value of DIT", ax, 1, 0, 7)
    combine_plot_generic_axes_pros_graph(metric_sum_dict.keys(), average_cbo, "Average value of CBO by year (all class)", "Average value of CBO", ax, 1, 1, 2)

    figManager = plt.get_current_fig_manager()
    figManager.resize(*figManager.window.maxsize())
    plt.show()

    fig1, ax1 = plt.subplots(2, 2)
    combine_plot_generic_axes_pros_graph(metric_sum_dict.keys(), average_noc, "Avergage value of NOC by year (all class)","Average value of NOC", ax1, 0, 0, 3)
    combine_plot_generic_axes_pros_graph(metric_sum_dict.keys(), average_rfc, "Average value of RFC by year (all class)", "Average value of RFC", ax1, 0, 1, 0)
    combine_plot_generic_axes_pros_graph(metric_sum_dict.keys(), average_fanin, "Average value of Fan-in by year (all class)","Average value of Fan-in", ax1, 1, 0, 0)
    combine_plot_generic_axes_pros_graph(metric_sum_dict.keys(), average_fanout, "Average value of Fan-out by year (all class)","Average value of Fan-out", ax1, 1, 1, 0)

    figManager = plt.get_current_fig_manager()
    figManager.resize(*figManager.window.maxsize())
    plt.show()

    fig, ax = plt.subplots(2, 2)

    combine_plot_generic_bar_graph(metric_sum_dict.keys(), sum_loc, "Total LOC by year (all class)", "Total LOC", ax, 0, 0, 0)
    combine_plot_generic_bar_graph(metric_sum_dict.keys(), average_of_wmc, "Average value of WMC by year (all class)", "Average value of WMC", ax, 0, 1, 14)
    combine_plot_generic_bar_graph(metric_sum_dict.keys(), average_dit, "Average value of DIT by year (all class)", "Average value of DIT", ax, 1, 0, 7)
    combine_plot_generic_bar_graph(metric_sum_dict.keys(), average_cbo, "Average value of CBO by year (all class)", "Average value of CBO", ax, 1, 1, 2)

    figManager = plt.get_current_fig_manager()
    figManager.resize(*figManager.window.maxsize())
    plt.show()

    fig, ax = plt.subplots(2, 2)

    combine_plot_generic_bar_graph(metric_sum_dict.keys(), average_noc, "Avergage value of NOC by year (all class)","Average value of NOC", ax, 0, 0, 3)
    combine_plot_generic_bar_graph(metric_sum_dict.keys(), average_rfc, "Average value of RFC by year (all class)", "Average value of RFC", ax, 0, 1, 0)
    combine_plot_generic_bar_graph(metric_sum_dict.keys(), list(average_fanin), "Average value of Fan-in by year (all class)","Average value of Fan-in", ax, 1, 0, 0)
    combine_plot_generic_bar_graph(metric_sum_dict.keys(), list(average_fanout), "Average value of Fan-out by year (all class)","Average value of Fan-out", ax, 1, 1, 0)

    figManager = plt.get_current_fig_manager()
    figManager.resize(*figManager.window.maxsize())
    plt.show()

    dic = metric_value_manipulate_for_class()

    metrics_variation = {
        "wmc": [],
        "fanin": [],
        "cbo": [],
        "fanin": [],
        "fanout": [],
        "dit": [],
        "rfc": [],
        "loc": [],
    }
    
    for value in dic.values():
        metrics_variation["wmc"].append(value[3])
        metrics_variation["fanin"].append(value[1])
        metrics_variation["cbo"].append(value[0])
        metrics_variation["fanout"].append(value[2])
        metrics_variation["dit"].append(value[4])
        metrics_variation["rfc"].append(value[5])
        metrics_variation["loc"].append(value[6])
    
    for key, value in metrics_variation.items():
        graph_title = "Metric (" + key + ") value variation for class"

        dic2 = {}
        limit_value = 0
        if str(key) == "wmc":
            for k, v in dic.items():
                if max(dic.get(k)[3]) > WMC_LIMIT:
                    dic2[k] = dic.get(k)[3]
            limit_value = WMC_LIMIT
        if str(key) == "cbo":
            for k, v in dic.items():
                if max(dic.get(k)[0]) > CBO_LIMIT:
                    dic2[k] = dic.get(k)[0]
            limit_value = CBO_LIMIT
        if str(key) == "dit":
            for k, v in dic.items():
                if max(dic.get(k)[4]) > DIT_LIMIT:
                    dic2[k] = dic.get(k)[4]
            limit_value = DIT_LIMIT
        if str(key) == "fanin":
            for k, v in dic.items():
                if max(dic.get(k)[1]) > FANIN_AVERAGE:
                    dic2[k] = dic.get(k)[1]
            limit_value = FANIN_AVERAGE
        if str(key) == "fanout":
            for k, v in dic.items():
                if max(dic.get(k)[2]) > FANOUT_AVERAGE:
                    dic2[k] = dic.get(k)[2]
            limit_value = FANOUT_AVERAGE
        if str(key) == "loc":
            for k, v in dic.items():
                if max(dic.get(k)[6]) > LOC_AVERAGE:
                    dic2[k] = dic.get(k)[6]
            limit_value = LOC_AVERAGE

        plot_boxplot_graph(value, dic, graph_title, limit_value)

        if limit_value != 0 and len(dic2) != 0:
            plot_boxplot_graph(dic2.values(), dic2, graph_title, limit_value)