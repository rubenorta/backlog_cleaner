#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv, sys, re, requests, json

from pprint import pprint

def clean_ticket(id):
	m = re.match(ur'#?(\d*)',id)
	if m and id:
		#print "True " + id + " / " + m.group(1)
		return m.group(1)
	else:
		#print "False " + id
		return False

backlog_file = sys.argv[1]
backlog_file_clean = "clean-" + backlog_file
login = sys.argv[2]
password = sys.argv[3]

print "Reading file... " + backlog_file 
output = open(backlog_file_clean, 'w')

with open(backlog_file,'rb') as file:
	# Leemos el fichero con todos los numeros de taquilla
	csv_reader = csv.reader(file, delimiter=',', quotechar='"')
	for ticket in csv_reader:
		ticket_id = clean_ticket(ticket[1])
		if ticket_id:
			# Validar si esta cerrada o no.
			r = requests.get('http://taquilla.antevenio.com/issues/' + str(ticket_id) + ".json", auth = (login, password))
			if r.status_code == 200:
				ticket_info = r.json()
				status = ticket_info['issue']['status']['id']
				if status not in (3,5,6):
					line = ','.join(ticket) + "\n"
					output.write(line)
				else:
					print "Task ID: " + str(ticket_id) + " REMOVED"





# Recorremos los tickets y validamos si la taquilla esta hecha o no
# Vemos la fecha de creación y modificación y lo metemos en NOTAS
# Grabamos el nuevo fichero