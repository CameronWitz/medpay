import MySQLdb as mysql

db = mysql.connect(user = 'medpay',
		passwd = 'meddiPASSpay4',
		db = 'medpay')
cur = db.cursor()

cur.execute('describe medicareMaster')

for t in cur.fetchall():
	print t[0]
print ' '

cur.execute('select distinct HCPCS_DESCRIPTION from medicareMaster')
descriptions = []
for t in cur.fetchall():
	descriptions.append(t[0]+'.')
print(len(descriptions))
with open("descriptions.txt", "w") as text_file:
	for d in descriptions:
		text_file.write("%s\n" % d)
