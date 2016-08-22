import psycopg2
import json

config = json.load(open('db.config'))

# Conn remoto
conn = psycopg2.connect(database = config['database'], user = config['user'], password = config['password'], host= config['host'], port = config['port'])

cur = conn.cursor()

# Todas as tabelas
cur.execute("SELECT relname FROM pg_class WHERE relkind='r' AND relname !~ '^(pg_|sql_)';")

# Todo o conteudo
cur.execute('SELECT * FROM "Minerios"')
rows = cur.fetchall()
for row in rows:
	print row