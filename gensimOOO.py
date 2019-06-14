from gensim.models import Word2Vec

model = Word2Vec.load("descriptionW2V.model")

done = False
while not done:
	query = input("Odd one out of (eg. breast_cancer, hospital): ")
	val = query.strip()
	q = val.split(" ")
	response = model.wv.doesnt_match(q)
	print("\n", response)
	print("\n")
