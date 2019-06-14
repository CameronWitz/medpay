import MySQLdb as mysql
import time

db = mysql.connect(
                   user='medpay',
                   passwd='meddiPASSpay4',
                   db='medpay')
cur = db.cursor()

print('')
print('Hello soldier. Welcome to the Medicare safe space. Find the perfect provider based on your demographics.')
print('...')
correct = 1 if raw_input('Let\'s begin? (y/n): ') in ['yes', 1, 'y'] else 0
if correct == 1:
  print('Good\n')
else:
  print('Too bad :p\n')

state = raw_input('Please provide abbreviated state symbol where you live (eg: CA for California): ')
print('\n')
# AGE
# - if person cares about senior citizen, return person with highest average age
age = raw_input('What\s your age bracket? (<65, 65-74, 74-84, 84+, skip): ')
print('\n')
# GENDER
# - ask if more comfortable with specific gender, or no pref. if more comfortable with one,
#   only show with that gender
gender = raw_input('What gender would you like your provider to be? (m, f, any): ')
print('\n')
# RACE
# - options: [white, black, asian, hispanic]
race = raw_input('What race do you want your provider to be?\nAdd all that are ok. (white, black, asian, hispanic, any): ')
print('\n')
# CONDITIONS
# - experience: [Alzheimers, Asthma, Cancer, Heart Failure, Kidney Disease, Depression, Diabetes ]
# (sort by that)
conditions = raw_input('Are you looking for a specialty?\nAdd as many separated by a space (no, alzheimers, asthma, cancer, heart-failure, kidney-disease, depression, diabetes): ')
print('\n')
# simple query example (state + gender)
# - select NPPES_PROVIDER_FIRST_NAME, NPPES_PROVIDER_LAST_ORG_NAME, NPPES_PROVIDER_STREET1, NPPES_PROVIDER_STREET2, NPPES_PROVIDER_CITY 
#   from providerMaster where NPPES_PROVIDER_GENDER='M' and NPPES_PROVIDER_STATE='CA' limit 10;

# sort based on age
# - select NPPES_PROVIDER_FIRST_NAME, NPPES_PROVIDER_LAST_ORG_NAME, NPPES_PROVIDER_STREET1, NPPES_PROVIDER_STREET2, NPPES_PROVIDER_CITY, BENEFICIARY_AVERAGE_AGE
# from providerMaster where NPPES_PROVIDER_GENDER='M' and NPPES_PROVIDER_STATE='CA' order by BENEFICIARY_AGE_LESS_65_COUNT desc limit 10;

# conditions + race
# select NPPES_PROVIDER_FIRST_NAME, NPPES_PROVIDER_LAST_ORG_NAME, NPPES_PROVIDER_STREET1, NPPES_PROVIDER_STREET2, NPPES_PROVIDER_CITY, BENEFICIARY_AVERAGE_AGE
# from providerMaster where NPPES_PROVIDER_GENDER='M' and NPPES_PROVIDER_STATE='CA' 
# order by BENEFICIARY_AGE_LESS_65_COUNT, BENEFICIARY_CC_ASTHMA_PERCENT, BENEFICIARY_CC_CANCER_PERCENT desc limit 10;

# all bools
has_gender = False if gender.strip() == "any" else True
has_age = False if age.strip() == "skip" else True 
has_race = False if race.strip() == "any" else True
has_conditions = False if conditions.strip().lower() == 'no' or conditions.strip().lower() == 'n' else True

# build up age
age_dict = {
  "<65": "BENEFICIARY_AGE_LESS_65_COUNT", 
  "65-74": "BENEFICIARY_AGE_65_74_COUNT", 
  "74-84": "BENEFICIARY_AGE_75_84_COUNT", 
  "84+": "BENEFICIARY_AGE_GREATER_84_COUNT"
}
age_res = age_dict[age] if has_age else ""

# build up race
race_dict = {
  "white": "BENEFICIARY_RACE_WHITE_COUNT",
  "black": "BENEFICIARY_RACE_BLACK_COUNT",
  "asian": "BENEFICIARY_RACE_API_COUNT",
  "hispanic": "BENEFICIARY_RACE_HISPANIC_COUNT"
}
race_res = ""
if has_race: 
  for i, v in enumerate(race.split()):
    race_res += race_dict[v.lower()] if i == 0 and not has_age else ", " + race_dict[v.lower()]

# build up conditions
conditions_dict = {
  "alzheimers": "BENEFICIARY_CC_ALZRDSD_PERCENT", 
  "asthma": "BENEFICIARY_CC_ASTHMA_PERCENT", 
  "cancer": "BENEFICIARY_CC_CANCER_PERCENT", 
  "heart-failure": "BENEFICIARY_CC_CHF_PERCENT",
  "kidney-disease": "BENEFICIARY_CC_CKD_PERCENT", 
  "depression": "BENEFICIARY_CC_DEPR_PERCENT", 
  "diabetes": "BENEFICIARY_CC_DIAB_PERCENT"
}
conditions_res = ""
if has_conditions:
  for i, v in enumerate(conditions.split()):
    conditions_res += conditions_dict[v.lower()] if i == 0 and not has_race else ", " + conditions_dict[v.lower()]

def format_val(val):
  return "'" + val + "'"

query = "select NPPES_PROVIDER_FIRST_NAME, NPPES_PROVIDER_LAST_ORG_NAME, NPPES_PROVIDER_STREET1, NPPES_PROVIDER_STREET2, NPPES_PROVIDER_CITY from providerMaster where NPPES_PROVIDER_STATE="\
  + format_val(state)\
  + ((" and NPPES_PROVIDER_GENDER=" + format_val(gender.upper())) if has_gender else "")\
  + ((" order by " + age_res + race_res + conditions_res) if has_age or has_race or has_conditions else "")\
  + " limit 5;"

print('Executing Query:\n')
print(query)
cur.execute(query)

print('We\'re all done! Here are the top 5 providers for you: \n')
print('-------------------------------')
print('First Name, Last Name, Address')
print('-------------------------------')
for first, last, st1, st2, city in cur.fetchall():
        print(first, last, st1, st2, city)

print('\n')
