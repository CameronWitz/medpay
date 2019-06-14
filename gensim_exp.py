from gensim.models import Word2Vec

model = Word2Vec.load("descriptionW2V.model")

done = False
while not done:
	query = input("Show me similar words to (eg. breast_cancer or hospital): ")
	val = query.strip()
	response = model.wv.most_similar(positive=[val])
	print("\n Word and Similarity Score")
	for r, v in response:
		print(r, v)
	
	cont = input("\n Continue? y or n: ")
	done = True if cont == "n" else False
	print("\n")
