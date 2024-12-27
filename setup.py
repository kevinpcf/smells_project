import subprocess
import os

# Progetti da elaborare
projects = ['expressjs/express','bower/bower','less/less.js','request/request','gruntjs/grunt','jquery/jquery','vuejs/vue','ramda/ramda','Leaflet/Leaflet','hexojs/hexo','chartjs/Chart.js','webpack/webpack','moment/moment','webtorrent/webtorrent','riot/riot']

# Per ogni progetto
for project in projects:

    # Ci spostiamo nella directory del progetto
    print('Il progetto',project,'è in fase di elaborazione!')
    os.chdir(project.split('/')[0])

    # Cloniamo il progetto da GitHub
    subprocess.run(['rm','-rf','uut'])
    subprocess.run(['git','clone','https://github.com/'+project+'.git','uut'])

    # Recuperiamo tutti i commit del progetto
    subprocess.run(['rm','-rf','commits-data'])
    subprocess.run(['mkdir','commits-data'])
    os.system('node commits.js > /dev/null')

    # Puliamo i dati dei commit del progetto
    subprocess.run(['rm','-rf','commits-clean'])
    subprocess.run(['mkdir','commits-clean'])
    subprocess.run(['node','clean.js'])

    # Raccogliamo le informazioni sugli smells che appaiono durante tutto il progetto
    subprocess.run(['rm','-f','report.txt'])
    os.system('node report.js > report.txt')

    # Raccogliamo le informazioni sui problemi (issues)
    subprocess.run(['rm','-f','issues.json'])
    os.system('node issues.js '+project+' > issues.json')

    # Combiniamo le informazioni di tracciamento degli smells e dei bug, e salviamo un primo tracciamento degli smells
    subprocess.run(['rm','-f','tracing_bugs_with_false_positive.txt'])
    os.system('node combine.js > tracing_bugs_with_false_positive.txt')

    # Rimuoviamo i bug che corrispondono a falsi positivi introdotti dall'algoritmo SZZ
    subprocess.run(['rm','-f','tracing_bugs.txt'])
    os.system('python3 remove_buggy_false_positive.py > tracing_bugs.txt')

    # Tracciamo i luoghi dei bug potenziali
    subprocess.run(['rm','-f','emplacements_bugs.txt'])
    os.system('python3 tracing_bugs_simple.py > emplacements_bugs.txt')

    # Tracciamo i luoghi dei bug potenziali in modo più ampio, considerando le dipendenze
    subprocess.run(['rm','-f','emplacements_bugs_large.txt'])
    os.system('python3 tracing_bugs_large.py > emplacements_bugs_large.txt')

    # Identifichiamo i file "smelly" (con cattive pratiche)
    subprocess.run(['rm','-f','smells_count.txt'])
    os.system('python3 set_smelly.py > smells_count.txt')

    # Visualizziamo i boxplot per ogni tipo di smell non booleano, quando possibile, per giustificare la soglia di peso
    subprocess.run(['Rscript','boxplot_smells_values.r'])

    # Rimettiamo in ordine i commit
    subprocess.run(['python3','commit_by_date.py'])

    # Torniamo nella directory principale
    os.chdir('..')
    print()

    # Aspettiamo (per evitare errori di limite API)
    subprocess.run(['sleep','3600'])
