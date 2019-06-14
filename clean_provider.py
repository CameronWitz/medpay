import re

file = open('provider_master.txt', 'r')
f = file.read()
f = re.sub('\t\t', '\t\N\t', f)
f = re.sub('\t\t', '\t\N\t', f)

n = open("provider_master_processed.txt","w+");
n.write(f);
n.close();
