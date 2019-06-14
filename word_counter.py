import pandas as pd
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

descriptions = pd.read_csv('descriptions.txt', sep = '\n')
descriptions = descriptions.values.tolist()

unique_w = set()
i = 0
for d in descriptions:
	print(i)
	words = d[0].split()
	for word in words:
		i += 1
		print(word)
		if word in stop_words or word == ".":
			pass
		else:
			if word not in unique_w:
				unique_w.add(word)

print(len(unique_w))
print(len(descriptions))
