import json
from pprint import pprint
from datetime import datetime
import math
import statistics

# Le but ici est de supprimer les faux positifs générés par l'algorithme SZZ chargé de récupérer les commits qui introduisent les bugs
# On va avoir 2 types de filtre. 
# Le premier concerne les bugs qu'impliquent un commits en particulier.
# Le deuxième concerne les commits impliqués dans un même bug
# On va stocker dans un dictionnaire, pour chaque commit, les issues à enlever, car susceptibles d'être des faux positifs
removed_issues_by_commit = {}

# Ouverture du fichier data.json qui contient les issues dans lesquels sont impliqués les commits (s'ils le sont)
with open("data.json") as json_data:
    data = json.load(json_data)
    json_data.close()

# Ouverture du fichier qui contient les issues (et notamment leur date d'apparition)
with open("issues.json") as json_issues:
    issues = json.load(json_issues)
    json_issues.close()

# Premier filtre : supprimer les bugs d'un commit trop éloignés de celui-ci
# Pour chaque commit du data
for i in range(len(data)):
    # S'il n'y a qu'un seul bug dans lequel est impliqué le commit, aucun traitement supplémentaire
    if(len(data[i]['buggy']) <= 1):
        continue
    # On récupère les numéros de bug
    nummero_bug_list = []
    for bug in data[i]['buggy']:
        numero_bug = int(bug.split(" ")[0])
        if (numero_bug not in nummero_bug_list):
            nummero_bug_list.append(numero_bug)
    if (len(nummero_bug_list) <= 1):
        continue
    commit = data[i]['commit']
    date_bug_list = []
    date_by_issue = {}
    for numero in nummero_bug_list:
        for issue in issues:
            if (numero == issue['number']):
                date_by_issue[numero] = datetime.strptime(issue['created_at'].split('Z')[0],"%Y-%m-%dT%H:%M:%S")
                date_bug_list.append(datetime.strptime(issue['created_at'].split('Z')[0],"%Y-%m-%dT%H:%M:%S"))
    date_bug_list.sort()
    min_date = date_bug_list[0]
    for issue in date_by_issue.keys():
        date_by_issue[issue] = (date_by_issue[issue] - min_date).total_seconds()
    for j in range(len(date_bug_list)):
        date_bug_list[j] = (date_bug_list[j] - min_date).total_seconds()
    median_date = statistics.median(date_bug_list)
    for j in range(len(date_bug_list)):
        date_bug_list[j] = abs(date_bug_list[j] - median_date)
    MAD = statistics.median(date_bug_list)
    for issue in date_by_issue.keys():
        if (date_by_issue[issue] > MAD + median_date):
            if (not commit in removed_issues_by_commit):
                removed_issues_by_commit[commit] = []
            if (not issue in removed_issues_by_commit[commit]):
                removed_issues_by_commit[commit].append(issue)

# Deuxième filtre : supprimer les commit potentiellement responsables d'un bug mais trop éloignés de celui-ci
# Pour chaque issue
for issue in issues:
    commit_of_issue = {}
    for i in range(len(data)):
        if(len(data[i]['buggy']) == 0):
            continue
        for bug in data[i]['buggy']:
            numero_bug = int(bug.split(" ")[0])
            if (numero_bug == issue['number']):
                commit_of_issue[data[i]['commit']] = datetime.strptime(data[i]['date'].split('.')[0],"%Y-%m-%dT%H:%M:%S")
    # S'il n'y a qu'un seul commit impliqué par le bug, aucun traitement supplémentaire
    if (len(commit_of_issue) <= 1):
        continue
    commit_date = []
    for commit in commit_of_issue.keys():
        commit_date.append(commit_of_issue[commit])
    commit_date.sort()
    max_date = commit_date[len(commit_date) - 1]
    for commit in commit_of_issue.keys():
        commit_of_issue[commit] = (max_date - commit_of_issue[commit]).total_seconds()
    for j in range(len(commit_date)):
        commit_date[j] = (max_date - commit_date[j]).total_seconds()
    median_date = statistics.median(commit_date)
    for j in range(len(commit_date)):
        commit_date[j] = abs(commit_date[j] - median_date)
    MAD = statistics.median(commit_date)
    for commit in commit_of_issue.keys():
        if(commit_of_issue[commit] > MAD + median_date):
            if (not commit in removed_issues_by_commit):
                removed_issues_by_commit[commit] = []
            if (not issue['number'] in removed_issues_by_commit[commit]):
                removed_issues_by_commit[commit].append(issue['number'])
#print(removed_issues_by_commit)

# Il faut enlever les bugs associés au commit qui correspondent à des faux positifs, et mettre à jour le fichier tracing_bugs.txt
with open("tracing_bugs_with_false_positive.txt") as file:
        tracing_bugs = file.readlines()
        file.close()
for i in range(len(tracing_bugs)):
    if(tracing_bugs[i].split(' ')[0]=='Fichier'):
        if('undefined' in tracing_bugs[i+1].split(' ')[1]):
            continue
        if('undefined' in tracing_bugs[i+2].split(' ')[1]):
            continue
        numero_issue = tracing_bugs[i+1].split(' ')[1].split('\n')[0]
        commit_candidat = tracing_bugs[i+2].split(' ')[1].split('\n')[0]
        if(commit_candidat in removed_issues_by_commit):
            if (int(numero_issue) in removed_issues_by_commit[commit_candidat]):
                #print(commit_candidat, numero_issue)
                continue
        print(tracing_bugs[i], end='')
        print(tracing_bugs[i+1], end='')
        print(tracing_bugs[i+2], end='')
        print(tracing_bugs[i+3], end='')
        print(tracing_bugs[i+4], end='')
        print(tracing_bugs[i+5], end='')

# On met également à jour le fichier data
for i in range(len(data)):
    if(len(data[i]['buggy']) == 0):
        continue
    if (data[i]['commit'] not in removed_issues_by_commit):
        continue
    bug_to_remove = removed_issues_by_commit[data[i]['commit']]
    bug_to_check = list(data[i]['buggy'])
    for j in reversed(range(len(bug_to_check))):
        numero_bug = int(bug_to_check[j].split(" ")[0])
        if (numero_bug in bug_to_remove):
            del data[i]['buggy'][j]
            #print(data[i]['buggy'][j])

with open('data_clean.json','w') as outfile:
    json.dump(data,outfile)
