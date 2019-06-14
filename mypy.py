# Test to see if we have mysqldb
import MySQLdb as mysql
import time

db = mysql.connect(
		   user='medpay',
		   passwd='meddiPASSpay4',
		   db='medpay')
cur = db.cursor()

# run a small query
cur.execute("describe medicareMaster")
columns = []
for row in cur.fetchall():
	columns.append(row[0])
print('Columns in Table medicareMaster')
print('')
for t in columns:
	print(t)

print('')
print('Hello there, and welcome to the MedPay')
print('...')
correct = 1 if raw_input('you have selected the price compare application, is this correct? ') in ['yes', 1, 'y'] else 0
if correct:
	print('Good\n')
else: 
	print('Too bad >:|\n')

state = raw_input('Please provide abbreviated state symbol where you live eg: CA for California: ')
desc = raw_input('Please provide a brief description of your procedure you would like to compare to: ')
desc = desc.split(' ')
temp = ""
for i, v in enumerate(desc):
	if i == len(desc)-1:
		temp += "'%"+v+"%'"
	else:
		temp += "'%"+v+"%'" + " and hcpcs_description like "

query = 'select distinct HCPCS_CODE, hcpcs_description from medicareMaster where hcpcs_description like ' + temp
print('Executing Query: \n', query)
cur.execute(query)
print('\nPlease survey the following results: \n')
print('HCPCS Code, Description')
for code, d in cur.fetchall():
	print(code, d)

codes = raw_input("\nEnter HCPCS code(s) of interest separated by spaces: ")
codes = codes.split(" ")
def codehelper(code):
	return "'" + code + "'"
codes = list(map(codehelper, codes))
codes = ",".join(codes)
codes = "("+codes+")"
# Fetch the avg submitted charge amount in state for the given HCPCS Code
query = "select avg(AVERAGE_SUBMITTED_CHRG_AMT) from medicareMaster where HCPCS_CODE in " + codes + " and NPPES_PROVIDER_STATE = " + "'"+state+"'" 
query += " group by hcpcs_code" 
print('Executing query: ', query)

cur.execute(query)
print('\nPlease survey the following results: \n')
for row in cur.fetchall():
	print(row)












