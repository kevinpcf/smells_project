import subprocess
import os

# Progetti da trattare
projects = ['gruntjs/grunt']

# Per ciascun progetto
for project in projects:

    # Ci si posiziona nella directory del progetto
    print('Il progetto', project, 'è in elaborazione!')
    os.chdir(project.split('/')[0])

    # Si generano i dati da analizzare (collegamenti tra fix dei bug e code smells)
    subprocess.run(['python3', 'smelly_buggy.py'])

    # Si generano le curve di sopravvivenza per ogni tipo di variabile e analisi, utilizzando un modello di Cox
    subprocess.run(['Rscript', 'analyze2.r'])

    # Si ritorna alla directory padre
    os.chdir('..')
    print()
