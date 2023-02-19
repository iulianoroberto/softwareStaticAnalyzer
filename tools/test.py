import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime
from filter_commits import filter_commits_by_year
import plotly.graph_objects as go
import seaborn as sns
import plotly.express as px
import pandas as pd

SYSTEM = "Java-WebSocket"
PROJECT_DIR = './project_to_analize/Java-WebSocket'
GIT_COMMITS_FILE = 'commits.txt'

def plot_selected_commits_timeline(commits_list):
    names = []
    dates = []
    for commit in commits_list:
        commit_details = commit.split(',')
        commit_date, commit_hash, commit_author = commit_details
        commit_date_two = commit_date[:10]
        names.append("Hash:"+commit_hash + " (published on " + commit_date_two + ")")
        dates.append(commit_date_two)
        # Convert date strings (e.g. 2014-10-18) to datetime
    dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]
    # Choose some nice levels
    levels = np.tile([-5, 5, -3, 3, -1, 1],
                    int(np.ceil(len(dates)/6)))[:len(dates)]
    # Create figure and plot a stem plot with the date
    fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
    ax.set_title(f"Selected commits of {SYSTEM.capitalize()}", fontweight="bold", fontsize=16, color='royalblue')
    ax.vlines(dates, 0, levels, color="tab:red")  # The vertical stems.
    ax.plot(dates, np.zeros_like(dates), "-o",
            color="royalblue", markerfacecolor="w")  # Baseline and markers on it.
    # annotate lines
    for d, l, r in zip(dates, levels, names):
        ax.annotate(r, xy=(d, l),
                    xytext=(-3, np.sign(l)*3), textcoords="offset points",
                    horizontalalignment="right",
                    verticalalignment="bottom" if l > 0 else "top",
                    fontweight="bold")
    # format xaxis with 4 month intervals
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    # remove y axis and spines
    ax.yaxis.set_visible(False)
    ax.spines[["left", "top", "right"]].set_visible(False)
    ax.margins(y=0.1)
    plt.show()

def plot_indicator(all_commits_len, filtered_commits_len):
    fig = go.Figure(go.Indicator(
        mode = "number+gauge+delta",
        gauge = {'shape': "bullet"},
        delta = {'reference': all_commits_len},
        value = filtered_commits_len,
        domain = {'x': [0.1, 1], 'y': [0.2, 0.9]},
        title = {"text": f"{SYSTEM.capitalize()}<br><span style='font-size:0.8em;color:gray'>Selected commits</span><br><span style='font-size:0.8em;color:gray'>on all commits</span>"}))
    fig.show()

def plot_commits_timeline(all_commits):
    commits_dic = {}
    for commit in all_commits:
        commit_details = commit.split(',')
        commit_date, commit_hash, commit_author = commit_details
        commit_date_two = commit_date[:7]
        keys = commits_dic.keys()
        if commit_date_two in keys:
            commits_dic[commit_date_two] = commits_dic[commit_date_two] + 1
        else:
            commits_dic[commit_date_two] = 1
    print(commits_dic)

    df = pd.DataFrame({'date':commits_dic.keys(), 'value':commits_dic.values()})
    print(df)
    fig = px.line(df, x='date', y='value', title=f'Commits pubblication for month ({SYSTEM})')

    fig.update_xaxes(rangeslider_visible=True)
    fig.show()

def main():
    commits_list = filter_commits_by_year()
    filtered_commits_len = len(commits_list)
    print(commits_list)
    all_commits = open(f'{PROJECT_DIR}/{GIT_COMMITS_FILE}', 'r+').readlines()
    all_commits_len = len(all_commits)
    #plot_indicator(all_commits_len, filtered_commits_len)
    plot_selected_commits_timeline(commits_list)
    plot_commits_timeline(all_commits)

main()