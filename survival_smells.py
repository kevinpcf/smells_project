import subprocess
import os

# Progetti da trattare
projects = ['vesparny/fair-analytics']

# Per ciascun progetto
for project in projects:

    # Ci spostiamo nella directory del progetto
    print('Il progetto',project,'è in fase di trattamento!')
    os.chdir(project.split('/')[0])

    # Generiamo i dati di sopravvivenza per ciascun tipo di smell
    subprocess.run(['python3','survival_code_smells.py','0.7'])

    # Generiamo le curve di sopravvivenza per ogni tipo di smell, utilizzando un modello di Cox
    subprocess.run(['Rscript','analyze.r'])

    # Ripetiamo l'operazione con una scala diversa (numero di commit invece del numero di giorni)
    subprocess.run(['python3','survival_code_smells_commit_scale.py','0.7'])
    subprocess.run(['Rscript','analyze_commit_scale.r'])

    # Torniamo nella directory principale
    os.chdir('..')
    print()
