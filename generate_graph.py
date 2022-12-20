import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Limit value: (WMC<=14, DIT<=7, NOC<=3, CBO<=2)

GIT_COMMITS_FILE = 'elenco_csv.txt'
ANALISYS_DIR = 'analysis'

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
        year = file_name.split('_')[3][:4]
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
                key = list(row[1])[1]
                cbo = list(row[1])[3]
                fanin = list(row[1])[5]
                fanout = list(row[1])[6]
                wmc = list(row[1])[7]
                dit = list(row[1])[8]
                rfc = list(row[1])[10]
                loc = list(row[1])[34]
                if key not in dic:
                    dic[key] = [[cbo],[fanin],[fanout],[wmc],[dit],[rfc],[loc]]
                else:
                    dic.get(key)[0].append(cbo)
                    dic.get(key)[1].append(fanin)
                    dic.get(key)[2].append(fanout)
                    dic.get(key)[2].append(wmc)
                    dic.get(key)[2].append(dit)
                    dic.get(key)[2].append(rfc)
                    dic.get(key)[2].append(loc)
    return dic



# Plot generic bar color graph
def combine_plot_generic_bar_graph(x_data, y_data, ylabel, title, ax, x_position, y_position, limit_value):
    ax[x_position, y_position].bar(x_data, y_data)
    ax[x_position, y_position].set_ylabel(ylabel)
    ax[x_position, y_position].set_title(title)
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
def plot_boxplot_graph(x_data, y_data):
    colors = ['rgba(93, 164, 214, 0.5)', 'rgba(255, 144, 14, 0.5)', 'rgba(44, 160, 101, 0.5)',
              'rgba(255, 65, 54, 0.5)', 'rgba(207, 114, 255, 0.5)', 'rgba(127, 96, 0, 0.5)']
    fig = go.Figure()
    for xd, yd, cls in zip(x_data, y_data, colors):
        fig.add_trace(go.Box(
            y=yd,
            name=xd,
            boxpoints='all',
            jitter=0.5,
            whiskerwidth=0.2,
            fillcolor=cls,
            marker_size=2,
            line_width=1)
        )
    fig.update_layout(
        title='Variation of metrics class by year',
        yaxis=dict(
            autorange=True,
            showgrid=True,
            zeroline=True,
            dtick=5,
            gridcolor='rgb(255, 255, 255)',
            gridwidth=1,
            zerolinecolor='rgb(255, 255, 255)',
            zerolinewidth=2,
        ),
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=100,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
        showlegend=True
    )
    fig.show()


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
    for key, value in dic.items():
        print(key)
        print(value)