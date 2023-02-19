from tools.filter_commits import filter_commits_by_year
from tools.CK_analysis import analize
from tools.generate_graph import *
#import tools.clone_analyzer as cla

def main():
    csv_class_file = []

    selected_commits = filter_commits_by_year()
    print(selected_commits)
    #analize(selected_commits)
    plotting()
    #dic = cla.cron_analyzing(selected_commits)
    #cla.plot_clones_by_year(dic)

main()





