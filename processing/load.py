import subprocess
import json

with open("creds.json") as file:
    creds = json.load(file)

loadCMD = '''mysql --host={} --user={} --password={}  --binary-mode=1 {} < data/raw.sql'''.format(creds['host'], creds['user'], creds['password'], creds['database'])
dumpCMD = '''mysqldump --host={} --user={} --password={} --default-character-set=utf8 backup > data/raw.sql'''.format(creds['host'], creds['user'], creds['password'])
dropCMD = '''mysql --host={} --user={} --password={} -e "DROP DATABASE {}"'''.format(creds['host'], creds['user'], creds['password'], creds['database'])
createCMD = '''mysql --host={} --user={} --password={} -e "CREATE DATABASE {}"'''.format(creds['host'], creds['user'], creds['password'], creds['database'])

subprocess.run(dumpCMD, shell=True, check=True)

try:
    subprocess.run(dropCMD, shell=True, check=True)
except:
    pass

subprocess.run(createCMD, shell=True, check=True)

subprocess.run(loadCMD, shell=True, check=True)