import psycopg2
import json
import urllib
import os
from testopencs import crop_new_image

config = json.load(open('db.config'))

# Conn remoto
conn = psycopg2.connect(database = config['database'], user = config['user'], password = config['password'], host= config['host'], port = config['port'])

cur = conn.cursor()

# Todas as tabelas
cur.execute("SELECT relname FROM pg_class WHERE relkind='r' AND relname !~ '^(pg_|sql_)';")

# Todo o conteudo
cur.execute('SELECT * FROM "Minerios"')
rows = cur.fetchall()
bd = list()

# Pega todo o conteudo do BD
for row in rows:
	minerio = dict()
	minerio['id'] = row[0]
	minerio['minerio'] = row[1]
	minerio['chapas'] = list()

	# Pegar as chapas
	cur.execute('SELECT * FROM "Chapas" WHERE "minerio_cd"=' + str(minerio['id']) + ';')
	chapas_rows = cur.fetchall()

	for chapa_row in chapas_rows:
		chapa = dict()
		chapa['id'] = chapa_row[0]
		# Pegar outras informacoes da chapa se precisar
		chapa['fotos'] = list()

		# Pegar as fotos
		cur.execute('SELECT * FROM "Fotos" WHERE "chapa_cd"=' + str(chapa['id']) + ';')
		fotos_rows = cur.fetchall()

		for foto_row in fotos_rows:
			foto = dict()
			foto['id'] = foto_row[0]
			foto['chapa_id'] = foto_row[1]
			foto['endereco'] = 'http://www.matheussilva.com/bdgeo/' + foto_row[2]
			foto['angulo'] = foto_row[3]
			foto['luz'] = foto_row[4]

			chapa['fotos'].append(foto)

		minerio['chapas'].append(chapa)
	bd.append(minerio)

# Iterando pelo BD
label_list = list()
arg_list = list()

for minerio in bd:
	folder = './' + minerio['minerio'] + '/'
	os.mkdir(folder)
	for chapa in minerio['chapas']:
		chapa_folder = folder + str(chapa['id']) + '/'
		os.mkdir(chapa_folder)
		images = list()
		nfotos = 0
		for foto in chapa['fotos']:
			image_path = chapa_folder + str(nfotos) + '.jpg'
			urllib.urlretrieve(foto['endereco'], image_path)
			nfotos += 1
