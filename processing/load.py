import subprocess

loadCMD = 'mysql --host=localhost --user=root --password=root  --binary-mode=1 nba < data/raw.sql'
dumpCMD = 'mysqldump --host=localhost --user=root --password=root --default-character-set=utf8 backup > data/raw.sql'
dropCMD = 'mysql --host=localhost --user=root --password=root -e "DROP DATABASE nba"'
createCMD = 'mysql --host=localhost --user=root --password=root -e "CREATE DATABASE nba"'

subprocess.run(dumpCMD, shell=True, check=True)

try:
    subprocess.run(dropCMD, shell=True, check=True)
except:
    subprocess.run(createCMD, shell=True, check=True)

subprocess.run(loadCMD, shell=True, check=True)