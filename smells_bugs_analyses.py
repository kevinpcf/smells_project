import subprocess
import os

# Progetti da trattare
projects = ['expressjs/express','bower/bower','less/less.js','request/request','gruntjs/grunt','jquery/jquery','vuejs/vue','ramda/ramda','Leaflet/Leaflet','hexojs/hexo','chartjs/Chart.js','webpack/webpack','moment/moment','webtorrent/webtorrent','riot/riot']

# Per ciascun progetto
for project in projects:

    # Ci spostiamo nella directory del progetto
    print('Il progetto',project,'è in fase di trattamento!')
    os.chdir(project.split('/')[0])

    # Generiamo i dati da analizzare (collegamenti tra bug risolti e code smells)
    subprocess.run(['python3','smelly_buggy.py'])

    # Generiamo le curve di sopravvivenza per ciascun tipo di variabile e tipo di analisi, utilizzando un modello di Cox
    subprocess.run(['Rscript','analyze2.r'])

    # Torniamo nella directory principale
    os.chdir('..')
    print()
